---
name: statsprocessor-maskgen
description: "Statsprocessor generates targeted dictionaries from corpora. Signals: password cracking, hash cracking, Markov statistics from dictionary, candidate generation by statistics, length range"
zh-signals: "Statsprocessor: 基于语料的定向字典生成。信号:密码破解,哈希破解,从字典生成马尔可夫统计,按统计生成候选,长度范围。"
when-to-use: "Use when preparing password or hash cracking attacks and you need candidate dictionaries that match a target organization's password habits. Requires a corpus or leaked wordlist plus the desired length range to learn Markov statistics and generate candidates."
---

# Statsprocessor

- Attack Category: C25 Password and Hash Cracking
- Upstream Repository: https://github.com/hashcat/statsprocessor
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/hashcat/statsprocessor && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./statsgen.bin wordlist.txt -o stats` | Generate Markov statistics from a wordlist |
| `./sp64.bin stats --threshold 30 -o candidates.txt` | Generate candidates by statistics |
| `--pw-min 8 --pw-max 12` | Length range |

## Attack Scenario Playbook

### Corpus-based targeted dictionary generation

```bash
./statsgen.bin leaked_corp_passwords.txt -o corp.stats && ./sp64.bin corp.stats -o corp_candidates.txt
# Generate candidates that closely match the target organization's password habits
```

## Notes

By the hashcat team; a Markov chain model learns from leaked passwords to produce high-hit-rate candidate dictionaries.
