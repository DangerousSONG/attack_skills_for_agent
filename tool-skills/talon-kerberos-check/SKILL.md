---
name: talon-kerberos-check
description: "Talon validates domain account existence. Signals: AD attack, domain penetration, domain controller"
zh-signals: "Talon: 域账户有效性验证。信号:ad攻击,域渗透,域控。"
when-to-use: >-
  Use during AD enumeration when you need to validate which domain accounts
  exist via Kerberos pre-authentication without triggering lockouts, or to find
  AS-REP roastable users.
---

# Talon

- Attack Category: C30 AD Domain Penetration and Domain Controller Attacks
- Upstream Repository: https://github.com/optiv/Talon
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/optiv/Talon && cd Talon
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 talon.py -D corp.local -U users.txt -p 'Pass123!'` | Kerberos pre-authentication enumeration |
| `-D d -U u.txt -p p.txt -A` | AS-REP roastable |
| `-t 10.0.0.1` | Domain controller |

## Attack Scenario Playbook

### Domain Account Existence Validation

```bash
python3 talon.py -D corp.local -U users.txt -p Pass1
# account enumeration without triggering alerts
```

## Notes

From optiv; enumerates accounts through Kerberos error codes.
