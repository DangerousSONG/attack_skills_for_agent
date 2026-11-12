---
name: bopscrk-smart-wordlist
description: "bopscrk: intelligently generates social engineering wordlists. Signals: password cracking, hash cracking, interactive targeted dictionary generation, keywords+years"
zh-signals: "bopscrk: 社工字典智能生成。信号:密码破解,哈希破解,交互生成定向字典,关键字+年份。"
when-to-use: >-
  Use before password cracking or spraying when you want to build a targeted
  wordlist from social-engineering details like names, birthdays, and hobbies.
---

# bopscrk

- Attack Category: C25 Hash and Password Cracking
- Upstream Repository: https://github.com/r3nt0n/bopscrk
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/r3nt0n/bopscrk && cd bopscrk
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 bopscrk.py -i` | Interactive targeted wordlist generation |
| `-w 'John,Target' -y 1990-2000` | Keywords + years |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Smart Social Engineering Wordlist Generation

```bash
python3 bopscrk.py -i
# name + birthday + hobbies → high-hit-rate wordlist
```

## Notes

Turns social engineering details into a targeted password wordlist.
