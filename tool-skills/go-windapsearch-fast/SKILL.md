---
name: go-windapsearch-fast
description: "go-windapsearch performs fast bulk LDAP enumeration. Signals: internal enumeration, network discovery, user enumeration, custom queries, full attribute output."
zh-signals: "go-windapsearch: 高速批量 LDAP 枚举。信号:内网枚举,网络发现,枚举用户,自定义查询,全属性输出。"
when-to-use: >-
  Use in AD or LDAP enumeration to quickly pull users, groups, and custom queries
  from one or multiple domain controllers.
---

# go-windapsearch

- Attack Category: C29 AD and LDAP Enumeration
- Upstream Repository: https://github.com/ropnop/go-windapsearch
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/ropnop/go-windapsearch@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `windapsearch -d corp.local -u svc -p pass --dc 10.0.0.1 --users` | Enumerate users |
| `--custom '(&(sAMAccountType=805306368)(adminCount=1))'` | Custom query |
| `--full` | Full attribute output |
| `--krb5 -k svc.ccache` | Ticket authentication |

## Attack Scenario Playbook

### High-Speed Bulk LDAP Enumeration

```bash
cat dcs.txt | xargs -I{} windapsearch -d corp.local -u svc -p pass --dc {} --users
# The Go version is fast under concurrency, pulling user lists across multiple DCs
```

## Notes

A Go rewrite of windapsearch, single file with no dependencies plus Kerberos ticket authentication, well suited to restricted environments.
