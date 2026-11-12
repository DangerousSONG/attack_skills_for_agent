---
name: pydictor-wordlist
description: "pydictor: Generates comprehensive password dictionaries. Signals: password cracking, hash cracking, basic dictionary generation, extended modes, plugins."
zh-signals: "pydictor: 全模式密码字典。信号:密码破解,哈希破解,基础字典生成,扩展模式,插件。"
when-to-use: >-
  Use when generating customized password dictionaries for cracking, including
  base, extended, plugin and social-engineering modes tailored to target information.
---

# pydictor

- Attack Category: C25 Hash and Password Cracking
- Upstream Repository: https://github.com/LandGrey/pydictor
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/LandGrey/pydictor && cd pydictor
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 pydictor.py -base d -len 6 8 -o out.txt` | Basic dictionary generation |
| `-extend word --level 4` | Extended mode |
| `-plug pid6` | Plugin |
| `--sedb` | Social engineering mode |

## Attack Scenario Playbook

### All-mode password dictionary

```bash
python3 pydictor.py --sedb
# Interactive social-engineering dictionary factory
```

## Notes

A powerful password dictionary generation framework with 50+ modes.