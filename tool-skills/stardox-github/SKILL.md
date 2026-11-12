---
name: stardox-github
description: "Stardox analyzes repository stargazers. Signals: attack surface, cloud assets, stargazer analysis"
zh-signals: "Stardox: 仓库 star 用户分析。信号:攻击面,云资产,stargazer 分析。"
when-to-use: >-
  Use when performing OSINT on an authorized GitHub repository and you want to analyze its
  stargazers to identify potentially relevant users.
---

# Stardox

- Attack Category: C05 External Attack Surface and Cloud Asset Exposure
- Upstream Repository: https://github.com/0xPrateek/Stardox
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/0xPrateek/Stardox && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 stardox.py -r target/repo` | Stargazer analysis |
| `-r repo -d` | Details |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Repository Stargazer Analysis

```bash
python3 stardox.py -r corp/internal
# who is watching the internal repository (internal staff?
```

## Notes

OSINT on GitHub repository stargazers.
