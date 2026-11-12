---
name: smbclient-ng-modern
description: "smbclient-ng: interactive SMB operations. Signals: internal enumeration, network discovery, modern SMB client, share browsing, download."
zh-signals: "smbclient-ng: 交互式 SMB 操作。信号:内网枚举,网络发现,现代 SMB 客户端,共享浏览,下载。"
when-to-use: "Use during internal network enumeration when you need an interactive modern SMB client to browse shares, download files, and use modules. Requires credentials or a session and target SMB hosts."
---

# smbclient-ng

- Attack Category: C29 Internal Network Discovery and Enumeration
- Upstream Repository: https://github.com/p0dalirius/smbclient-ng
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install smbclientng
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `smbclient-ng -H 10.0.0.5 -u svc -p pass -d corp.local` | Modern SMB client |
| `use shares` | Share browsing |
| `get secrets.txt` | Download |
| `put file` | Upload |
| `modules` | Post-exploitation modules |

## Attack Scenario Playbook

### Interactive SMB Operations

```bash
smbclient-ng -H dc01 -u svc -p pass -d corp
# Made by p0dalirius, a modern replacement for smbclient
```

## Notes

A modern SMB client with a colored interface and a module system.
