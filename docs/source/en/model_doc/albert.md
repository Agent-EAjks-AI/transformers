<!--Copyright 2020 The HuggingFace Team. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

⚠️ Note that this file is in Markdown but contain specific syntax for our doc-builder (similar to MDX) that may not be
rendered properly in your Markdown viewer.

-->

# ALBERT

<div class="flex flex-wrap space-x-1">
<img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-DE3412?style=flat&logo=pytorch&logoColor=white">
<img alt="TensorFlow" src="https://img.shields.io/badge/TensorFlow-FF6F00?style=flat&logo=tensorflow&logoColor=white">
<img alt="Flax" src="https://img.shields.io/badge/Flax-29a79b.svg?style=flat&logo=data:image/png;base64,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
">
<img alt="SDPA" src="https://img.shields.io/badge/SDPA-DE3412?style=flat&logo=pytorch&logoColor=white">
</div>

## Overview

The ALBERT model was proposed in [ALBERT: A Lite BERT for Self-supervised Learning of Language Representations](https://huggingface.co/papers/1909.11942) by Zhenzhong Lan, Mingda Chen, Sebastian Goodman, Kevin Gimpel, Piyush Sharma,
Radu Soricut. It presents two parameter-reduction techniques to lower memory consumption and increase the training
speed of BERT:

- Splitting the embedding matrix into two smaller matrices.
- Using repeating layers split among groups.

The abstract from the paper is the following:

*Increasing model size when pretraining natural language representations often results in improved performance on
downstream tasks. However, at some point further model increases become harder due to GPU/TPU memory limitations,
longer training times, and unexpected model degradation. To address these problems, we present two parameter-reduction
techniques to lower memory consumption and increase the training speed of BERT. Comprehensive empirical evidence shows
that our proposed methods lead to models that scale much better compared to the original BERT. We also use a
self-supervised loss that focuses on modeling inter-sentence coherence, and show it consistently helps downstream tasks
with multi-sentence inputs. As a result, our best model establishes new state-of-the-art results on the GLUE, RACE, and
SQuAD benchmarks while having fewer parameters compared to BERT-large.*

This model was contributed by [lysandre](https://huggingface.co/lysandre). This model jax version was contributed by
[kamalkraj](https://huggingface.co/kamalkraj). The original code can be found [here](https://github.com/google-research/ALBERT).

## Usage tips

- ALBERT is a model with absolute position embeddings so it's usually advised to pad the inputs on the right rather
  than the left.
- ALBERT uses repeating layers which results in a small memory footprint, however the computational cost remains
  similar to a BERT-like architecture with the same number of hidden layers as it has to iterate through the same
  number of (repeating) layers.
- Embedding size E is different from hidden size H justified because the embeddings are context independent (one embedding vector represents one token), whereas hidden states are context dependent (one hidden state represents a sequence of tokens) so it's more logical to have H >> E. Also, the embedding matrix is large since it's V x E (V being the vocab size). If E < H, it has less parameters.
- Layers are split in groups that share parameters (to save memory).
Next sentence prediction is replaced by a sentence ordering prediction: in the inputs, we have two sentences A and B (that are consecutive) and we either feed A followed by B or B followed by A. The model must predict if they have been swapped or not.
- The `head_mask` argument is ignored when using all attention implementation other than "eager". If you have a `head_mask` and want it to have effect, load the model with `XXXModel.from_pretrained(model_id, attn_implementation="eager")`  

### Using Scaled Dot Product Attention (SDPA)

PyTorch includes a native scaled dot-product attention (SDPA) operator as part of `torch.nn.functional`. This function 
encompasses several implementations that can be applied depending on the inputs and the hardware in use. See the 
[official documentation](https://pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html) 
or the [GPU Inference](https://huggingface.co/docs/transformers/main/en/perf_infer_gpu_one#pytorch-scaled-dot-product-attention)
page for more information.

SDPA is used by default for `torch>=2.1.1` when an implementation is available, but you may also set 
`attn_implementation="sdpa"` in `from_pretrained()` to explicitly request SDPA to be used.

```
from transformers import AlbertModel
model = AlbertModel.from_pretrained("albert/albert-base-v1", torch_dtype=torch.float16, attn_implementation="sdpa")
...
```

For the best speedups, we recommend loading the model in half-precision (e.g. `torch.float16` or `torch.bfloat16`).

On a local benchmark (GeForce RTX 2060-8GB, PyTorch 2.3.1, OS Ubuntu 20.04) with `float16`, we saw the 
following speedups during training and inference.

#### Training for 100 iterations

|batch_size|seq_len|Time per batch (eager - s)| Time per batch (sdpa - s)| Speedup (%)| Eager peak mem (MB)| sdpa peak mem (MB)| Mem saving (%)|
|----------|-------|--------------------------|--------------------------|------------|--------------------|-------------------|---------------|
|2         |256    |0.028                     |0.024                     |14.388      |358.411             |321.088            |11.624         |
|2         |512    |0.049                     |0.041                     |17.681      |753.458             |602.660            |25.022         |
|4         |256    |0.044                     |0.039                     |12.246      |679.534             |602.660            |12.756         |
|4         |512    |0.090                     |0.076                     |18.472      |1434.820            |1134.140           |26.512         |
|8         |256    |0.081                     |0.072                     |12.664      |1283.825            |1134.140           |13.198         |
|8         |512    |0.170                     |0.143                     |18.957      |2820.398            |2219.695           |27.062         |

#### Inference with 50 batches

|batch_size|seq_len|Per token latency eager (ms)|Per token latency SDPA (ms)|Speedup (%) |Mem eager (MB)|Mem BT (MB)|Mem saved (%)|
|----------|-------|----------------------------|---------------------------|------------|--------------|-----------|-------------|
|4         |128    |0.083                       |0.071                      |16.967      |48.319        |48.45      |-0.268       |
|4         |256    |0.148                       |0.127                      |16.37       |63.4          |63.922     |-0.817       |
|4         |512    |0.31                        |0.247                      |25.473      |110.092       |94.343     |16.693       |
|8         |128    |0.137                       |0.124                      |11.102      |63.4          |63.66      |-0.409       |
|8         |256    |0.271                       |0.231                      |17.271      |91.202        |92.246     |-1.132       |
|8         |512    |0.602                       |0.48                       |25.47       |186.159       |152.564    |22.021       |
|16        |128    |0.252                       |0.224                      |12.506      |91.202        |91.722     |-0.567       |
|16        |256    |0.526                       |0.448                      |17.604      |148.378       |150.467    |-1.388       |
|16        |512    |1.203                       |0.96                       |25.365      |338.293       |271.102    |24.784       |

This model was contributed by [lysandre](https://huggingface.co/lysandre). This model jax version was contributed by
[kamalkraj](https://huggingface.co/kamalkraj). The original code can be found [here](https://github.com/google-research/ALBERT).


## Resources


The resources provided in the following sections consist of a list of official Hugging Face and community (indicated by 🌎) resources to help you get started with AlBERT. If you're interested in submitting a resource to be included here, please feel free to open a Pull Request and we'll review it! The resource should ideally demonstrate something new instead of duplicating an existing resource.


<PipelineTag pipeline="text-classification"/>


- [`AlbertForSequenceClassification`] is supported by this [example script](https://github.com/huggingface/transformers/tree/main/examples/pytorch/text-classification).


- [`TFAlbertForSequenceClassification`] is supported by this [example script](https://github.com/huggingface/transformers/tree/main/examples/tensorflow/text-classification).

- [`FlaxAlbertForSequenceClassification`] is supported by this [example script](https://github.com/huggingface/transformers/tree/main/examples/flax/text-classification) and [notebook](https://colab.research.google.com/github/huggingface/notebooks/blob/main/examples/text_classification_flax.ipynb).
- Check the [Text classification task guide](../tasks/sequence_classification) on how to use the model.


<PipelineTag pipeline="token-classification"/>


- [`AlbertForTokenClassification`] is supported by this [example script](https://github.com/huggingface/transformers/tree/main/examples/pytorch/token-classification).


- [`TFAlbertForTokenClassification`] is supported by this [example script](https://github.com/huggingface/transformers/tree/main/examples/tensorflow/token-classification) and [notebook](https://colab.research.google.com/github/huggingface/notebooks/blob/main/examples/token_classification-tf.ipynb).



- [`FlaxAlbertForTokenClassification`] is supported by this [example script](https://github.com/huggingface/transformers/tree/main/examples/flax/token-classification).
- [Token classification](https://huggingface.co/course/chapter7/2?fw=pt) chapter of the 🤗 Hugging Face Course.
- Check the [Token classification task guide](../tasks/token_classification) on how to use the model.

<PipelineTag pipeline="fill-mask"/>

- [`AlbertForMaskedLM`] is supported by this [example script](https://github.com/huggingface/transformers/tree/main/examples/pytorch/language-modeling#robertabertdistilbert-and-masked-language-modeling) and [notebook](https://colab.research.google.com/github/huggingface/notebooks/blob/main/examples/language_modeling.ipynb).
- [`TFAlbertForMaskedLM`] is supported by this [example script](https://github.com/huggingface/transformers/tree/main/examples/tensorflow/language-modeling#run_mlmpy) and [notebook](https://colab.research.google.com/github/huggingface/notebooks/blob/main/examples/language_modeling-tf.ipynb).
- [`FlaxAlbertForMaskedLM`] is supported by this [example script](https://github.com/huggingface/transformers/tree/main/examples/flax/language-modeling#masked-language-modeling) and [notebook](https://colab.research.google.com/github/huggingface/notebooks/blob/main/examples/masked_language_modeling_flax.ipynb).
- [Masked language modeling](https://huggingface.co/course/chapter7/3?fw=pt) chapter of the 🤗 Hugging Face Course.
- Check the [Masked language modeling task guide](../tasks/masked_language_modeling) on how to use the model.

<PipelineTag pipeline="question-answering"/>

- [`AlbertForQuestionAnswering`] is supported by this [example script](https://github.com/huggingface/transformers/tree/main/examples/pytorch/question-answering) and [notebook](https://colab.research.google.com/github/huggingface/notebooks/blob/main/examples/question_answering.ipynb).
- [`TFAlbertForQuestionAnswering`] is supported by this [example script](https://github.com/huggingface/transformers/tree/main/examples/tensorflow/question-answering) and [notebook](https://colab.research.google.com/github/huggingface/notebooks/blob/main/examples/question_answering-tf.ipynb).
- [`FlaxAlbertForQuestionAnswering`] is supported by this [example script](https://github.com/huggingface/transformers/tree/main/examples/flax/question-answering).
- [Question answering](https://huggingface.co/course/chapter7/7?fw=pt) chapter of the 🤗 Hugging Face Course.
- Check the [Question answering task guide](../tasks/question_answering) on how to use the model.

**Multiple choice**

- [`AlbertForMultipleChoice`] is supported by this [example script](https://github.com/huggingface/transformers/tree/main/examples/pytorch/multiple-choice) and [notebook](https://colab.research.google.com/github/huggingface/notebooks/blob/main/examples/multiple_choice.ipynb).
- [`TFAlbertForMultipleChoice`] is supported by this [example script](https://github.com/huggingface/transformers/tree/main/examples/tensorflow/multiple-choice) and [notebook](https://colab.research.google.com/github/huggingface/notebooks/blob/main/examples/multiple_choice-tf.ipynb).

- Check the  [Multiple choice task guide](../tasks/multiple_choice) on how to use the model.


## AlbertConfig

[[autodoc]] AlbertConfig

## AlbertTokenizer

[[autodoc]] AlbertTokenizer
    - build_inputs_with_special_tokens
    - get_special_tokens_mask
    - create_token_type_ids_from_sequences
    - save_vocabulary

## AlbertTokenizerFast

[[autodoc]] AlbertTokenizerFast

## Albert specific outputs

[[autodoc]] models.albert.modeling_albert.AlbertForPreTrainingOutput

[[autodoc]] models.albert.modeling_tf_albert.TFAlbertForPreTrainingOutput

<frameworkcontent>
<pt>

## AlbertModel

[[autodoc]] AlbertModel
    - forward

## AlbertForPreTraining

[[autodoc]] AlbertForPreTraining
    - forward

## AlbertForMaskedLM

[[autodoc]] AlbertForMaskedLM
    - forward

## AlbertForSequenceClassification

[[autodoc]] AlbertForSequenceClassification
    - forward

## AlbertForMultipleChoice

[[autodoc]] AlbertForMultipleChoice

## AlbertForTokenClassification

[[autodoc]] AlbertForTokenClassification
    - forward

## AlbertForQuestionAnswering

[[autodoc]] AlbertForQuestionAnswering
    - forward

</pt>

<tf>

## TFAlbertModel

[[autodoc]] TFAlbertModel
    - call

## TFAlbertForPreTraining

[[autodoc]] TFAlbertForPreTraining
    - call

## TFAlbertForMaskedLM

[[autodoc]] TFAlbertForMaskedLM
    - call

## TFAlbertForSequenceClassification

[[autodoc]] TFAlbertForSequenceClassification
    - call

## TFAlbertForMultipleChoice

[[autodoc]] TFAlbertForMultipleChoice
    - call

## TFAlbertForTokenClassification

[[autodoc]] TFAlbertForTokenClassification
    - call

## TFAlbertForQuestionAnswering

[[autodoc]] TFAlbertForQuestionAnswering
    - call

</tf>
<jax>

## FlaxAlbertModel

[[autodoc]] FlaxAlbertModel
    - __call__

## FlaxAlbertForPreTraining

[[autodoc]] FlaxAlbertForPreTraining
    - __call__

## FlaxAlbertForMaskedLM

[[autodoc]] FlaxAlbertForMaskedLM
    - __call__

## FlaxAlbertForSequenceClassification

[[autodoc]] FlaxAlbertForSequenceClassification
    - __call__

## FlaxAlbertForMultipleChoice

[[autodoc]] FlaxAlbertForMultipleChoice
    - __call__

## FlaxAlbertForTokenClassification

[[autodoc]] FlaxAlbertForTokenClassification
    - __call__

## FlaxAlbertForQuestionAnswering

[[autodoc]] FlaxAlbertForQuestionAnswering
    - __call__

</jax>
</frameworkcontent>


