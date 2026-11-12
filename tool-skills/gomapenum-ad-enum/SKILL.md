---
name: gomapenum-ad-enum
description: "GoMapEnum enumerates Active Directory across all protocols. Signals: AD attack, domain penetration, LDAP enumeration, ticket attacks, O365 enumeration."
zh-signals: "GoMapEnum: AD 全协议枚举。信号:ad攻击,域渗透,LDAP 枚举,票据攻击,O365 枚举。"
when-to-use: "Use during Active Directory penetration testing to enumerate users and services across multiple protocols including LDAP, ticket attacks, and O365. Requires target domain credentials or a user list."
---

# GoMapEnum

- Attack Category: C30 AD Domain Penetration and Domain Controller Attacks
- Upstream Repository: https://github.com/nodauf/GoMapEnum
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/nodauf/GoMapEnum@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `goMapEnum ldap -u svc -p pass -d corp.local -t 10.0.0.1` | LDAP enumeration |
| `kerberos -u u.txt -p p.txt -d corp.local` | Ticket attacks |
| `oauth -t user@corp.com -p pass` | O365 enumeration |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### AD enumeration across all protocols

```bash
goMapEnum ldap -u svc -p pass -d corp.local
# LDAP, Kerberos and OAuth in one tool
```

## Notes

Go AD enumeration framework, multi-protocol.
