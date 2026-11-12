---
name: dharma-grammar-fuzz
description: "dharma: protocol/file format fuzz sample generation. Signals: pwn, binary exploitation, syntax-based sample generation, counter mode, debugging."
zh-signals: "dharma: 协议/文件格式 fuzz 样本生成。信号:pwn,二进制利用,按语法生成样本,计数器模式,调试。"
when-to-use: "Use when fuzzing a protocol or file format and you need grammar-based test case generation driven by .dg syntax definitions to feed AFL-style fuzzing engines."
---

# dharma

- Attack Category: C46 Fuzzing and Vulnerability Discovery
- Upstream Repository: https://github.com/MozillaSecurity/dharma
- Upstream License: MPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/MozillaSecurity/dharma && cd dharma && pip install .
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python dharma.py -g grammars/dom.dg -n 100` | Generate samples from the grammar |
| `-c 4` | Counter mode |
| `--loglevel debug` | Debug |

## Attack Scenario Playbook

### Protocol/file format fuzz sample generation

```bash
python dharma.py -g grammars/css.dg -n 1000 > cases.txt
# By Mozilla; template grammar generates high-coverage samples
```

## Notes

Mozilla's grammar-based fuzzing framework that describes formats with .dg syntax to generate samples, used with AFL-style engines.
