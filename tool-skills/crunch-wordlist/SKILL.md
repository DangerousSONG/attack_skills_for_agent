---
name: crunch-wordlist
description: "crunch: Generates targeted mask-based dictionaries. Signals: password cracking, hash cracking, charset generation, numeric only, mask template."
zh-signals: "crunch: 掩码定向字典生成。信号:密码破解,哈希破解,按字符集生成,纯数字,掩码模板。"
when-to-use: >-
  Use when you need to generate targeted password or hash-cracking dictionaries
  from known character sets, numeric ranges, or mask templates such as
  admin@@@@.
---

# crunch

- Attack Category: C25 Hash and Password Cracking
- Upstream Repository: https://sourceforge.net/projects/crunch-wordlist
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install crunch
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `crunch 8 10 -f /usr/share/crunch/charset.lst lalpha-numeric` | Generate from a charset |
| `crunch 6 8 0123456789 -o num.txt` | Digits only |
| `crunch 8 8 -t admin@@@@` | Mask template |
| `-s start -e end` | Start/end range |
| `-b 500mb` | Split by size |

## Attack Scenario Playbook

### Targeted Mask-Based Dictionary Generation

```bash
crunch 10 10 -t '2024@@@@@' -o candidates.txt  # Company prefix + year pattern mask brute force
```

## Notes

A classic dictionary generator; the mask template (-t) suits targeted brute forcing when part of the password structure is known.
