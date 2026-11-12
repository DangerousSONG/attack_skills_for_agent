---
name: enum4linux-ng
description: "enum4linux-ng: anonymous/credential domain information harvesting and quick workgroup discovery. Signals: internal enumeration, network discovery, all modules, with credentials."
zh-signals: "enum4linux-ng: 匿名/凭据双模式域信息收割、工作组环境快速摸底。信号:内网枚举,网络发现,所有模块,带凭据。"
when-to-use: "Use enum4linux-ng when enumerating SMB/RPC/LDAP on a Windows host or domain, either anonymously or with credentials, to harvest users, shares, password policy, and OS details for internal discovery."
---

# enum4linux-ng

- Attack Category: C29 Internal Network Discovery and Enumeration
- Upstream Repository: https://github.com/cddmp/enum4linux-ng
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/cddmp/enum4linux-ng && cd enum4linux-ng && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./enum4linux-ng.py 10.0.0.5` | Full SMB/RPC/LDAP enumeration |
| `-A` | All modules |
| `-u user -p pass` | With credentials |
| `-R/-S/-U` | Respectively: users / shares / policies |
| `-w workgroup` | Specify the workgroup |
| `-oJ out.json` | JSON output |
| `-p 139,445` | Ports |

## Attack Scenario Playbook

### Harvesting domain information in anonymous/credential dual mode

```bash
./enum4linux-ng.py 10.0.0.5 -oJ enum.json
# Output: domain SID / user table / share table / password policy / OS / printers, ready to feed password spraying
```

### Quick survey of a workgroup environment

```bash
./enum4linux-ng.py 192.168.1.10 -w WORKGROUP
```

## Notes

A Python rewrite of enum4linux; the JSON output suits agent pipeline parsing; the LDAP module requires a reachable domain controller.
