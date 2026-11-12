---
name: adidnsdump-ldap-enum
description: "adidnsdump: harvests AD DNS records to discover servers. Signals: internal network enumeration, network discovery, list zones only, resolve records to IPs, include deleted records"
zh-signals: "adidnsdump: AD DNS 记录收割(发现服务器)。信号:内网枚举,网络发现,只列出区域,解析记录获取 IP,含已删除记录。"
when-to-use: "Use during internal AD enumeration to harvest integrated DNS records and discover servers and unregistered assets. Requires domain credentials and a DC address, optionally listing zones or including deleted records."
---

# adidnsdump

- Attack Category: C29 AD and LDAP Enumeration
- Upstream Repository: https://github.com/dirkjanm/adidnsdump
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install git+https://github.com/dirkjanm/adidnsdump.git or apt install adidnsdump
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `adidnsdump -u 'corp.local\svc' -p 'pass' dc01.corp.local` | Dump all AD-integrated DNS records |
| `-u user@corp.local -p pass --print-zones` | List zones only |
| `-r` | Resolve records to IPs |
| `--include-tombstoned` | Include deleted records |

## Attack Scenario Playbook

### AD DNS Record Harvesting (Server Discovery)

```bash
adidnsdump -u 'corp.local\svc' -p 'Pass1' dc01.corp.local -r
# Get full resolution for *.corp.local, focus on non-production domains such as dev/test/backup
```

## Notes

Made by dirkjanm. AD-integrated DNS is often the most complete inventory of in-domain hosts, including unregistered assets, so its reconnaissance value is extremely high.
