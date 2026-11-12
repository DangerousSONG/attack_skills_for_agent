---
name: windapsearch-ldap-ad
description: "windapsearch: Custom LDAP queries. Signals: internal network enumeration, network discovery, enumerate users, domain admins only, computers."
zh-signals: "windapsearch: 自定义 LDAP 查询。信号:内网枚举,网络发现,枚举用户,仅域管,计算机。"
when-to-use: >-
  Use when enumerating an Active Directory domain over LDAP for users, domain admins, computers, gMSA accounts or custom attribute queries that may reveal credentials.
---

# windapsearch

- Attack Category: C29 AD and LDAP Enumeration
- Upstream Repository: https://github.com/ropnop/windapsearch
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/ropnop/windapsearch && cd windapsearch && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python windapsearch.py -d corp.local -u svc -p pass --dc-ip 10.0.0.1 --users` | Enumerate users |
| `--da` | Domain Admins only |
| `--computers` | Computers |
| `--gmsa` | gMSA |
| `--psobject` | Custom LDAP query |
| `--terms userdescription` | Search attribute keywords |

## Attack Scenario Playbook

### Custom LDAP Queries

```bash
python windapsearch.py -d corp.local -u svc -p pass --dc-ip 10.0.0.1 --psobject "(&(objectCategory=person)(description=*pass*))"
# Initial passwords are often written in the description field
```

## Notes

ropnop's Swiss Army knife for LDAP queries, with common queries built in plus support for arbitrary filters, available for both Python 2 and 3.
