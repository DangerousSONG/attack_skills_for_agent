---
name: mentalist-wordlist
description: "Mentalist: GUI dictionary factory. Signals: password cracking, hash cracking, visual dictionary generation, mutation."
zh-signals: "Mentalist: GUI 字典工厂。信号:密码破解,哈希破解,可视化字典生成,变异。"
when-to-use: "Use when interactively building a targeted password dictionary with mutations for cracking engagements."
---

# Mentalist

- Attack Category: C25 Hash and Password Cracking
- Upstream Repository: https://github.com/sc0tfree/mentalist
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/sc0tfree/mentalist && cd mentalist && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 mentalist.py` | Visual dictionary generation |
| `-w base.txt -m 'A1@'` | Mutation |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### GUI Dictionary Factory

```bash
python3 mentalalist.py
# Interactively build a high-hit-rate dictionary
```

## Notes

A visual password dictionary generator.
