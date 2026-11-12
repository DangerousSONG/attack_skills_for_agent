---
name: omnibus-osint
description: "Fast IP/domain intelligence. Signals: email collection, employee info, OSINT CLI, IP intelligence, domain intelligence."
zh-signals: "Omnibus: IP/域名快速情报。信号:邮箱收集,员工信息,OSINT CLI,IP 情报,域名情报。"
when-to-use: >-
  Use when collecting OSINT on IPs, domains, emails or employees and you need
  a fast CLI combining IP and domain intelligence.
---

# Omnibus

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/InQuest/Omnibus
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/InQuest/Omnibus && cd Omnibus && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 omnibus.py` | OSINT CLI |
| `intel 1.2.3.4` | IP intelligence |
| `intel evil.com` | Domain intelligence |
| `report` | Generate report |

## Attack Scenario Playbook

### Fast IP/domain intelligence

```bash
python3 omnibus.py intel corp.com
# By InQuest, aggregates threat intelligence
```

## Notes

OSINT CLI by InQuest, simple and efficient.
