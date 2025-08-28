# coding=utf-8
# Copyright 2024 The Qwen team, Alibaba Group and the HuggingFace Inc. team. All rights reserved.
#
# This code is based on EleutherAI's GPT-NeoX library and the GPT-NeoX
# and OPT implementations in this library. It has been modified from its
# original forms to accommodate minor architectural differences compared
# to GPT-NeoX and OPT used by the Meta AI team that trained the model.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""PyTorch Qwen2MoE model."""

import math
from typing import Optional, Union

import torch
import torch.nn.functional as F

from torch import nn

from ...generation import GenerationMixin

from ...modeling_layers import (
    GenericForQuestionAnswering,
    GenericForSequenceClassification,
    GenericForTokenClassification,
    GradientCheckpointingLayer,
)

from .configuration_qwen2_moe import Qwen2MoeConfig
from ..llama.modeling_llama import LlamaRMSNorm, LlamaRotaryEmbedding, LlamaAttention, rotate_half, apply_rotary_pos_emb
from ..gemma.modeling_gemma import GemmaMLP
from ..mixtral.modeling_mixtral import MixtralModel, MixtralPreTrainedModel, MixtralForCausalLM, MixtralDecoderLayer, MixtralNaiveMoe

class Qwen2MoeRMSNorm(LlamaRMSNorm):
    pass

class Qwen2MoeRotaryEmbedding(LlamaRotaryEmbedding):
    pass

class Qwen2MoeMLP(GemmaMLP):
    def __init__(self, config, intermediate_size=None):
        super().__init__()
        self.config = config
        self.hidden_size = config.hidden_size
        self.intermediate_size = config.intermediate_size if intermediate_size is None else intermediate_size
        self.gate_proj = nn.Linear(self.hidden_size, self.intermediate_size, bias=False)
        self.up_proj = nn.Linear(self.hidden_size, self.intermediate_size, bias=False)
        self.down_proj = nn.Linear(self.intermediate_size, self.hidden_size, bias=False)
        self.act_fn = ACT2FN[config.hidden_act]

class Qwen2MoeAttention(LlamaAttention):
    def __init__(self, config: Qwen2MoeConfig, layer_idx: int):
        super().__init__(config, layer_idx)
        self.sliding_window = config.sliding_window if config.layer_types[layer_idx] == "sliding_attention" else None

        self.q_proj = nn.Linear(
            config.hidden_size, config.num_attention_heads * self.head_dim, bias=config.qkv_bias
        )
        self.k_proj = nn.Linear(
            config.hidden_size, config.num_key_value_heads * self.head_dim, bias=config.qkv_bias
        )
        self.v_proj = nn.Linear(
            config.hidden_size, config.num_key_value_heads * self.head_dim, bias=config.qkv_bias
        )
        self.o_proj = nn.Linear(
            config.num_attention_heads * self.head_dim, config.hidden_size, bias=False
        )
    

class Qwen2MoeNaiveMoe(nn.ModuleList):
    def __init__(self, config):
        super().__init__()
        self.top_k = config.num_experts_per_tok
        self.num_experts = config.num_experts
        self.norm_topk_prob = config.norm_topk_prob # FIXME: remove this once I check all qwen2 don't use this
        for _ in range(self.num_experts):
            self += [Qwen2MoeMLP(config, intermediate_size=config.moe_intermediate_size)]

    def forward(self, hidden_states, routing_weights):
        routing_weights = F.softmax(routing_weights, dim=1, dtype=torch.float)
        routing_weights, selected_experts = torch.topk(routing_weights, self.top_k, dim=-1)
        if self.norm_topk_prob: # ONLY DIFF WITH MIXTRAL FOR NOW
            routing_weights /= routing_weights.sum(dim=-1, keepdim=True)
        # we cast back to the input dtype
        routing_weights = routing_weights.to(hidden_states.dtype)
        final_hidden_states = torch.zeros_like(hidden_states, device=hidden_states.device)
        # One hot encode the selected experts to create an expert mask
        # this will be used to easily index which expert is going to be sollicitated
        expert_mask = torch.nn.functional.one_hot(selected_experts, num_classes=self.num_experts).permute(2, 1, 0)

        expert_hit = torch.greater(expert_mask.sum(dim=(-1, -2)), 0).nonzero()
        for expert_idx in expert_hit:
            expert_layer = self[expert_idx]
            idx, top_x = torch.where(expert_mask[expert_idx].squeeze(0))
            # Index the correct hidden states and compute the expert hidden state for
            # the current expert. We need to make sure to multiply the output hidden
            # states by `routing_weights` on the corresponding tokens (top-1 and top-2)
            current_state = hidden_states[None, top_x].reshape(-1, hidden_states.shape[-1])
            current_hidden_states = expert_layer(current_state) * routing_weights[top_x, idx, None]

            # However `index_add_` only support torch tensors for indexing so we'll use
            # the `top_x` tensor here.
            final_hidden_states.index_add_(0, top_x, current_hidden_states.to(hidden_states.dtype))
        return final_hidden_states

class Qwen2MoeSparseMoeBlock(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.num_experts = config.num_experts
        self.top_k = config.num_experts_per_tok
        self.norm_topk_prob = config.norm_topk_prob

        # gating
        self.gate = nn.Linear(config.hidden_size, config.num_experts, bias=False)
        self.experts = Qwen2MoeNaiveMoe(config=config)

        self.shared_expert = Qwen2MoeMLP(config, intermediate_size=config.shared_expert_intermediate_size)
        self.shared_expert_gate = torch.nn.Linear(config.hidden_size, 1, bias=False)

    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        """ """
        batch_size, sequence_length, hidden_dim = hidden_states.shape
        hidden_states = hidden_states.view(-1, hidden_dim)
        # router_logits: (batch * sequence_length, n_experts)
        router_logits = self.gate(hidden_states)
        final_hidden_states = self.experts(hidden_states, router_logits).reshape(batch_size, sequence_length, hidden_dim)

        shared_expert_output = self.shared_expert(hidden_states)
        shared_expert_output = F.sigmoid(self.shared_expert_gate(hidden_states)) * shared_expert_output

        final_hidden_states = final_hidden_states + shared_expert_output
        final_hidden_states = final_hidden_states.reshape(batch_size, sequence_length, hidden_dim)
        return final_hidden_states, router_logits


class Qwen2MoeDecoderLayer(MixtralDecoderLayer):
    def __init__(self, config: Qwen2MoeConfig, layer_idx: int):
        super().__init__(config, layer_idx)
        self.self_attn = Qwen2MoeAttention(config, layer_idx)
        if (layer_idx not in config.mlp_only_layers) and (
            config.num_experts > 0 and (layer_idx + 1) % config.decoder_sparse_step == 0
        ):
            self.mlp = Qwen2MoeSparseMoeBlock(config)
        else:
            self.mlp = Qwen2MoeMLP(config, intermediate_size=config.intermediate_size)
        del self.block_sparse_moe

    def forward(
        self,
        hidden_states: torch.Tensor,
        position_embeddings: tuple[torch.Tensor, torch.Tensor],
        attention_mask: Optional[torch.Tensor] = None,
        position_ids: Optional[torch.LongTensor] = None,
        past_key_values: Optional[tuple[torch.Tensor]] = None,
        cache_position: Optional[torch.LongTensor] = None,
        **kwargs: Unpack[TransformersKwargs],
    ) -> torch.FloatTensor:
        residual = hidden_states

        hidden_states = self.input_layernorm(hidden_states)

        # Self Attention
        hidden_states, _ = self.self_attn(
            hidden_states=hidden_states,
            position_embeddings=position_embeddings,
            attention_mask=attention_mask,
            position_ids=position_ids,
            past_key_values=past_key_values,
            cache_position=cache_position,
            **kwargs,
        )
        hidden_states = residual + hidden_states

        # Fully Connected
        residual = hidden_states
        hidden_states = self.post_attention_layernorm(hidden_states)
        hidden_states= self.mlp(hidden_states)
        if isinstance(hidden_states, tuple):
            hidden_states = hidden_states[0]
        hidden_states = residual + hidden_states
        return hidden_states



@auto_docstring
class Qwen2MoePreTrainedModel(MixtralPreTrainedModel):
    pass


@auto_docstring
class Qwen2MoeModel(MixtralModel):
    def __init__(self, config: Qwen2MoeConfig):
        super().__init__(config)
        self.layers = nn.ModuleList(
            [Qwen2MoeDecoderLayer(config, layer_idx) for layer_idx in range(config.num_hidden_layers)]
        )
        self.norm = Qwen2MoeRMSNorm(config.hidden_size, eps=config.rms_norm_eps)
        self.rotary_emb = Qwen2MoeRotaryEmbedding(config=config)


class Qwen2MoeForCausalLM(MixtralForCausalLM, GenerationMixin):
    _tied_weights_keys = ["lm_head.weight"]
    _tp_plan = {"lm_head": "colwise_rep"}
    _pp_plan = {"lm_head": (["hidden_states"], ["logits"])}

    def __init__(self, config):
        super().__init__(config)
        self.num_experts = config.num_experts
        self.model = Qwen2MoeModel(config)


class Qwen2MoeForSequenceClassification(GenericForSequenceClassification, Qwen2MoePreTrainedModel): ...


class Qwen2MoeForTokenClassification(GenericForTokenClassification, Qwen2MoePreTrainedModel): ...


class Qwen2MoeForQuestionAnswering(GenericForQuestionAnswering, Qwen2MoePreTrainedModel): ...


__all__ = [
    "Qwen2MoeForCausalLM",
    "Qwen2MoeForQuestionAnswering",
    "Qwen2MoeModel",
    "Qwen2MoePreTrainedModel",
    "Qwen2MoeForSequenceClassification",
    "Qwen2MoeForTokenClassification",
]
