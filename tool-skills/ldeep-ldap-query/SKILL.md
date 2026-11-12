---
name: ldeep-ldap-query
description: "ldeep performs lightweight LDAP queries as a BloodHound alternative. Signals: internal enumeration, network discovery, list domain users, detailed information, gMSA enumeration."
zh-signals: "ldeep: 轻量 LDAP 查询替代 bloodhound。信号:内网枚举,网络发现,列域用户,详细信息,gMSA 账户枚举。"
when-to-use: >-
  Use when enumerating an Active Directory domain over LDAP and you need fast user, trust, or
  gMSA listings without deploying BloodHound.
---

# ldeep

- Attack Category: C29 AD and LDAP Enumeration
- Upstream Repository: https://github.com/franc-pentest/ldeep
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install git+https://github.com/franc-pentest/ldeep
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `ldeep ldap -u svc -p pass -d corp.local -s ldap://10.0.0.1 users` | List domain users |
| `ldeep ... users -v` | Detailed information |
| `ldeep ... enum_gmsa` | gMSA account enumeration |
| `ldeep ... trusts` | Domain trust queries |
| `ldeep krb5 -u svc -k svc.ccache users` | Kerberos authenticated queries |

## Attack Scenario Playbook

### Lightweight LDAP Queries as a BloodHound Alternative

```bash
ldeep ldap -u svc -p pass -d corp.local -s 10.0.0.1 users -v | tee users.txt
# Produce a domain user list fast, much quicker than BH
```

## Notes

A lightweight LDAP enumeration tool with friendly output formatting that supports Kerberos ticket authentication.
