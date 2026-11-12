---
name: ad-ldap-enum-ldap
description: "ad-ldap-enum: Crowe LDAP enumeration tool. Signals: internal network enumeration, network discovery, LDAP full enumeration"
zh-signals: "ad-ldap-enum: Crowe 出品 LDAP 枚举。信号:内网枚举,网络发现,LDAP 全枚举。"
when-to-use: >-
  Use when enumerating users, groups, computers, OUs, and GPOs from an LDAP
  directory such as Active Directory; provide the LDAP URL and valid
  credentials and export the results for further analysis.
---

# ad-ldap-enum

- Attack Category: C29 Internal Network Discovery and Enumeration
- Upstream Repository: https://github.com/CroweCybersecurity/ad-ldap-enum
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/CroweCybersecurity/ad-ldap-enum && cd ad-ldap-enum
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 ad-ldap-enum.py -l ldap://10.0.0.1 -u svc@corp.local -p pass -m` | Full LDAP enumeration |
| `-l url -u u -p p -d` | Details |
| `-o out/` | Output |

## Attack Scenario Playbook

### Crowe LDAP Enumeration

```bash
python3 ad-ldap-enum.py -l ldap://dc01 -u svc@corp.local -p pass
# Export users/groups/computers/OU/GPO
```

## Notes

By CroweCyber, a simple and direct LDAP enumeration tool.
