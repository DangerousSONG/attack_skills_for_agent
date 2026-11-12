---
name: teamsuserenum-teams
description: "TeamsUserEnum enumerates valid Teams users. Signals: email collection, employee information, Teams user enumeration, threads"
zh-signals: "TeamsUserEnum: Teams 用户有效性枚举。信号:邮箱收集,员工信息,Teams 用户枚举,线程。"
when-to-use: "Use to validate Microsoft Teams accounts and enumerate employees from a candidate email list during OSINT."
---

# TeamsUserEnum

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/immense-mountain/TeamsUserEnum
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/immense-mountain/TeamsUserEnum && cd TeamsUserEnum && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 teamsuserenum.py -u users.txt -d corp.com` | Teams user enumeration |
| `-u u.txt -d d -t 10` | Threads |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Teams User Validity Enumeration

```bash
python3 teamsuserenum.py -u names.txt -d corp.com
# Uses error codes to determine whether a user exists, leaving no logs
```

## Notes

Microsoft Teams user enumeration for in-domain personnel discovery.
