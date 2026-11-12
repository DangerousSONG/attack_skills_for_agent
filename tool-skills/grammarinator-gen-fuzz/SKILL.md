---
name: grammarinator-gen-fuzz
description: "grammarinator performs ANTLR grammar-driven fuzzing. Signals: pwn, binary exploitation, test sample generation, mutation of parsed samples."
zh-signals: "grammarinator: ANTLR 语法驱动 fuzz。信号:pwn,二进制利用,生成测试样本,解析已有样本变异。"
when-to-use: >-
  Use when generating grammar-aware fuzz test cases from an ANTLR grammar;
  process the grammar and generate samples, or parse and mutate existing
  inputs.
---

# grammarinator

- Attack Category: C46 Fuzzing and Vulnerability Discovery
- Upstream Repository: https://github.com/renatahodovan/grammarinator
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install grammarinator
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `grammarinator-process grammar.g4 -o out/` | Generate a generator from an ANTLR grammar |
| `grammarinator-generate -l out/Generator.py -r out/unparser.py -o tests/ -n 100` | Generate test samples |
| `grammarinator-parse ...` | Parse and mutate existing samples |

## Attack Scenario Playbook

### ANTLR grammar-driven fuzzing

```bash
grammarinator-process JavaScript.g4 -o gen/ && grammarinator-generate -l gen/ -o cases/ -n 500
# Turns any ANTLR grammar into a fuzzing generator
```

## Notes

Automatically generates fuzz samples from ANTLR grammars with no hand-written generator; coverage is higher than with random mutation.
