---
name: adpeas-quickwin
description: "adPEAS: performs quick low-privilege AD assessment. Signals: ad attack, domain pentest, one-click AD privilege escalation enumeration, all modules, report output"
zh-signals: "adPEAS: 低权限 AD 快速摸底。信号:ad攻击,域渗透,一键 AD 提权枚举,全模块,输出报告。"
when-to-use: >-
  Use during domain penetration testing when you have low-privilege AD
  credentials and need one-click enumeration of Kerberoast, AS-REP, sensitive
  groups, password policy, and GPOs, with actionable privilege escalation
  recommendations.
---

# adPEAS

- Attack Category: C30 AD and Lateral Movement
- Upstream Repository: https://github.com/ajm4n/adpeas
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/ajm4n/adpeas && cd adpeas
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 adPEAS.py -d corp.local -u svc -p pass -dc 10.0.0.1` | One-click AD privilege escalation enumeration |
| `-a` | All modules |
| `-m kerberoast` | Single module (Kerberoast/AS-REP/BloodHound) |
| `-o report.txt` | Output report |

## Attack Scenario Playbook

### Quick low-privilege AD assessment

```bash
python3 adPEAS.py -d corp.local -u svc -p pass -dc 10.0.0.1 -a
# Kerberoast/AS-REP/sensitive groups/password policy/GPO all in one run
```

## Notes

Automated AD privilege escalation enumeration, the domain counterpart of linPEAS, outputting directly actionable escalation recommendations.
