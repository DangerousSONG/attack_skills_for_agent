---
name: duplicut-dedup
description: "duplicut: second-level deduplication of 50GB dictionaries. Signals: password cracking, hash cracking, large dictionary deduplication, length filtering, memory limit."
zh-signals: "duplicut: 50GB 字典秒级去重。信号:密码破解,哈希破解,大字典去重,长度过滤,内存限制。"
when-to-use: >-
  Use when preparing very large password or hash-cracking dictionaries and you
  need fast deduplication with length filtering under a bounded memory budget.
---

# duplicut

- Attack Category: C25 Hash and Password Cracking
- Upstream Repository: https://github.com/nil0x42/duplicut
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/nil0x42/duplicut && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./duplicut wordlist.txt -o clean.txt` | Large dictionary deduplication |
| `-i in -o out -l 8` | Length filtering |
| `-m 10000000` | Memory limit |

## Attack Scenario Playbook

### Second-level deduplication of a 50GB dictionary

```bash
./duplicut big.txt -o clean.txt
# Memory-mapped, a hundred times faster than sort -u
```

## Notes

Large dictionary deduplication tool from nil0x42.