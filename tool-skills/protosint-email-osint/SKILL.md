---
name: protosint-email-osint
description: "Email leak intelligence. Signals: email collection, employee info, phone number social database query, domain-associated email detection."
zh-signals: "ProtOSINT: 邮箱泄露情报。信号:邮箱收集,员工信息,手机号社工库查询,域名关联邮箱探测。"
when-to-use: >-
  Use during social engineering reconnaissance when you need to check an email,
  phone number, or domain against breach and paste sources for leaked data.
---

# ProtOSINT

- Attack Category: C03 OSINT Intelligence Gathering
- Upstream Repository: https://github.com/pixelbubble/ProtOSINT
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/pixelbubble/ProtOSINT && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 protOSINT.py -m mail -e target@mail.com` | Multi-source email OSINT (HIBP / paste sites) |
| `-m phone -p +1234` | Phone number social engineering database lookup |
| `-m domain -d t.com` | Domain-associated email discovery |
| `-o report.txt` | Output |

## Attack Scenario Playbook

### Email leak intelligence

```bash
python3 protOSINT.py -m mail -e ceo@corp.com
# Historical leaked passwords / breach incidents to judge credential stuffing and phishing material
```

## Notes

Aggregated breach lookups for emails, phone numbers, and domains; no API key required, ideal for pre-social-engineering intelligence.
