---
name: nbtscan-netbios
description: "nbtscan: Quick internal network hostname census. Signals: internal network enumeration, network discovery, NetBIOS name scanning, use port 137 recursively, detailed."
zh-signals: "nbtscan: 内网主机名快速普查。信号:内网枚举,网络发现,NetBIOS 名称扫描,使用 137 端口递归,详细。"
when-to-use: "Use on the first pass of internal network enumeration to quickly map NetBIOS hostnames, domains, and roles via port 137."
---

# nbtscan

- Attack Category: C29 Internal Network Discovery and Enumeration
- Upstream Repository: https://github.com/scallywag/nbtscan
- Upstream License: LGPL-2.1 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install nbtscan
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `nbtscan 10.0.0.0/24` | NetBIOS name scanning |
| `-r` | Recurse using port 137 |
| `-v` | Verbose |

## Attack Scenario Playbook

### Quick Internal Network Hostname Census

```bash
nbtscan -r 10.0.0.0/24
# Yields hostnames/domains/MACs, more information than a ping sweep, and quickly finds DCs/file servers
```

## Notes

A long-standing NetBIOS enumeration tool; run it first on day one of an internal engagement, hostnames directly expose roles.
