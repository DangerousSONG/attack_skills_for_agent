---
name: h8mail-breach-hunting
description: "h8mail checks emails in breach databases and prepares bulk employee credential stuffing. Signals: email collection, employee information, JSON output."
zh-signals: "h8mail: 查邮箱是否在泄露库中出现、批量员工邮箱撞库前置。信号:邮箱收集,员工信息,JSON 输出。"
when-to-use: >-
  Use during email OSINT to check whether addresses appear in breach databases and
  prepare credential-stuffing lists.
---

# h8mail

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/khast3x/h8mail
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install h8mail
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `-t victim@corp.com` | Single-email breach lookup |
| `-t targets.txt` | Bulk |
| `-q 'CorpName'` | Search breach collections by keyword |
| `-ch chase_keys.txt` |  chase mode (multi-field correlation) |
| `-o results.json` | JSON output |
| `-lb /opt/breach/` | Local breach database lookup |

## Attack Scenario Playbook

### Check Whether an Email Appears in Breach Databases

```bash
h8mail -t ceo@corp.com -o out.json
cat out.json | jq -r '.[].breaches[]?' | sort -u
```

### Preparation for Bulk Employee Email Credential Stuffing

```bash
h8mail -t emails.txt -lb /data/breachcompilation/ -o creds.json
```

## Notes

Queries public sources such as HaveIBeenPwned/EmoLogger; pair it with a local breach database for offline lookups.
