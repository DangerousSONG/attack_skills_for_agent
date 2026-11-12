---
name: activedirectoryenum-ad
description: "ActiveDirectoryEnum: performs AD enumeration and attack surface analysis. Signals: ad attack, domain pentest, BloodHound"
zh-signals: "ActiveDirectoryEnum: AD 枚举+攻击面分析。信号:ad攻击,域渗透,BloodHound。"
when-to-use: "Use ActiveDirectoryEnum when you have domain credentials and need to enumerate Active Directory objects and analyze attack paths, optionally exporting BloodHound-compatible data for a domain penetration test."
---

# ActiveDirectoryEnum

- Attack Category: C30 AD Domain Penetration and Domain Controller Attacks
- Upstream Repository: https://github.com/CasperGN/ActiveDirectoryEnum
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install activedirectoryenum
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `active-directory-enum -u svc -p pass -d corp.local -dc 10.0.0.1` | AD enumeration + attack surface |
| `-u u -p p -d d -dc ip -s` | BloodHound |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### AD Enumeration and Attack Surface Analysis

```bash
active-directory-enum -u svc -p pass -d corp.local
# enumeration + vulnerability paths + report output
```

## Notes

AD enumeration and attack path analysis in one tool.
