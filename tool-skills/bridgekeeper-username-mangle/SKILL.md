---
name: bridgekeeper-username-mangle
description: "BridgeKeeper: Converts HR rosters into sprayable password dictionaries. Signals: email harvesting, employee information, name-to-username rule generation, custom format."
zh-signals: "BridgeKeeper: HR 名单变喷洒字典。信号:邮箱收集,员工信息,人名→用户名规则生成,指定格式。"
when-to-use: >-
  Use when you have an employee name list and a corporate domain and need to generate username and password variants following common naming conventions for spraying.
---

# BridgeKeeper

- Attack Category: C03 OSINT Intelligence Gathering
- Upstream Repository: https://github.com/0xZDH/BridgeKeeper
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/0xZDH/BridgeKeeper && cd BridgeKeeper
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python bridgekeeper.py -f names.txt -d corp.com` | Name-to-username rule generation |
| `-f names.txt -d corp.com --format first.last` | Custom format |
| `-o users.txt` | Output |
| `--formats` | List all rules |

## Attack Scenario Playbook

### Turn an HR roster into a spray dictionary

```bash
python bridgekeeper.py -f employees.txt -d corp.com -o users.txt
# John Smith→john.smith/jsmith/j.smith all variants
```

## Notes

After collecting an employee roster via OSINT, generates usernames following corporate naming conventions; a prerequisite tool for spraying/brute force.
