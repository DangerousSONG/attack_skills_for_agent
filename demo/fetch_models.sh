#!/usr/bin/env bash
# 从 ModelScope 拉取 demo/CLI 所需模型到 demo/models/（huggingface.co 直连不通时的替代渠道）
set -e
cd "$(dirname "$0")"
BASE=https://modelscope.cn/models
get() { # $1=repo $2=file
  mkdir -p "models/$1/$(dirname "$2")"
  [ -s "models/$1/$2" ] && { echo "skip $1/$2"; return; }
  echo "get  $1/$2"
  curl -fL --retry 3 -o "models/$1/$2" "$BASE/$1/resolve/master/$2"
}
R=BAAI/bge-small-zh-v1.5
for f in config.json modules.json sentence_bert_config.json special_tokens_map.json \
         tokenizer.json tokenizer_config.json vocab.txt 1_Pooling/config.json model.safetensors; do
  get "$R" "$f"
done
R=BAAI/bge-small-en-v1.5
for f in config.json modules.json sentence_bert_config.json special_tokens_map.json \
         tokenizer.json tokenizer_config.json vocab.txt 1_Pooling/config.json model.safetensors; do
  get "$R" "$f"
done
R=BAAI/bge-reranker-v2-m3
for f in config.json sentencepiece.bpe.model special_tokens_map.json tokenizer.json \
         tokenizer_config.json model.safetensors; do
  get "$R" "$f"
done
# bge-m3: 多语言 1024 维, 语料中英混排时的 L1 默认模型; 权重只有 pytorch_model.bin(2.2GB), 无 safetensors
R=BAAI/bge-m3
for f in config.json modules.json sentence_bert_config.json config_sentence_transformers.json \
         special_tokens_map.json tokenizer.json tokenizer_config.json sentencepiece.bpe.model \
         1_Pooling/config.json pytorch_model.bin; do
  get "$R" "$f"
done
echo DONE
