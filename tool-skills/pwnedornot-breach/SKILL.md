---
name: pwnedornot-breach
description: "PwnedOrNot: Queries breach databases for email passwords. Signals: email collection, employee information, email breach query, batch, breached only."
zh-signals: "PwnedOrNot: 邮箱泄露库查询拿明文口令。信号:邮箱收集,员工信息,邮箱泄露查询,批量,仅受泄。"
when-to-use: >-
  Use when you have target email addresses and want to check breach databases
  for leaked credentials, including plaintext passwords, individually or in batch.
---

# PwnedOrNot

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/thewhiteh4t/pwnedOrNot
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/thewhiteh4t/pwnedOrNot && cd pwnedOrNot
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 pwnedornot.py -e victim@mail.com` | Email breach lookup |
| `-f emails.txt` | Batch |
| `-b` | Breached only |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Breach database lookup for email plaintext passwords

```bash
python3 pwnedornot.py -e ceo@corp.com
# The HaveIBeenPwned part that includes plaintext password leaks
```

## Notes

From whiteh4t; an enhanced HIBP that returns the leaked password portion.
