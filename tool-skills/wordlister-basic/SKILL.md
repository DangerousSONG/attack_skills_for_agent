---
name: wordlister-basic
description: "Wordlister: Keyword combination wordlist. Signals: password cracking, hash cracking, patterns."
zh-signals: "Wordlister: 关键词组合字典。信号:密码破解,哈希破解,模式。"
when-to-use: "Use Wordlister when you need to generate a password wordlist by combining target-specific keywords with case, digit, and symbol mutations before hash cracking."
---

# Wordlister

- Attack Category: C25 Hash and Password Cracking
- Upstream Repository: https://github.com/4n4nk3/Wordlister
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/4n4nk3/Wordlister && cd Wordlister
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 wordlister.py -w 'word1 word2' -m 8 -o out.txt` | Combination wordlist |
| `-w words -m min --cap -l -n` | Patterns |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Keyword Combination Wordlist

```bash
python3 wordlister.py -w 'admin target 2024'
# Combinations of case, digits and symbols
```

## Notes

Lightweight keyword combination wordlist generation.
