---
name: ldapmonitor-live-enum
description: "ldapmonitor watches AD changes to find new privileged accounts. Signals: internal enumeration, network discovery, real-time LDAP monitoring, filter conditions, change details."
zh-signals: "ldapmonitor: 实时盯 AD 变更(找新特权账号)。信号:内网枚举,网络发现,实时监控 LDAP 变更,过滤条件,显示变更详情。"
when-to-use: "Use ldapmonitor when you need real-time monitoring of LDAP changes on a domain controller to detect newly created privileged accounts or live administrative activity during an AD engagement."
---

# ldapmonitor

- Attack Category: C29 AD and LDAP Enumeration
- Upstream Repository: https://github.com/p0dalirius/ldapmonitor
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/p0dalirius/ldapmonitor && cd ldapmonitor && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 ldapmonitor.py -d corp.local -u svc -p 'pass' --dc-ip 10.0.0.1` | Real-time LDAP change monitoring |
| `--search '(&(objectClass=user))'` | Filter conditions |
| `-v` | Show change details |

## Attack Scenario Playbook

### Watch AD changes in real time (find new privileged accounts)

```bash
python3 ldapmonitor.py -d corp.local -u svc -p pass --dc-ip 10.0.0.1
# Watch new user/group changes alongside other attacks to spot operational activity windows
```

## Notes

By p0dalirius; continuously monitors LDAP changes (create, delete, modify) on the domain controller, useful during the persistence phase to observe defensive responses.
