---
name: narthex-pass-gen
description: "narthex: Dictionary enhancement pipeline. Signals: password cracking, hash cracking, combination, insertion, leet transformation."
zh-signals: "narthex: 字典增强流水线。信号:密码破解,哈希破解,组合,插入,leet 变换。"
when-to-use: "Use narthex when you need to enhance an existing password dictionary through combination, insertion, and leet transformations before hash cracking, as an alternative to hashcat rules."
---

# narthex

- Attack Category: C25 Hash and Password Cracking
- Upstream Repository: https://github.com/MichaelConstant/narthex
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/MichaelConstant/narthex && cd narthex && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./nhance -w wordlist.txt -o out.txt` | Dictionary enhancement |
| `./ncombi -i in -o out` | Combination |
| `./ninsert -i in -c 123` | Insertion |
| `./nleet -i in` | leet transformation |

## Attack Scenario Playbook

### Dictionary Enhancement Pipeline

```bash
cat base.txt | ./nhance | ./nleet > final.txt
# The full combination/insertion/transformation toolkit
```

## Notes

A dictionary manipulation toolset, an alternative to hashcat rules.
