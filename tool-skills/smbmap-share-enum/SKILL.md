---
name: smbmap-share-enum
description: "smbmap: harvests sensitive share files and checks writable shares. Signals: internal enumeration, network discovery, anonymous or current session list shares, specified credentials."
zh-signals: "smbmap: 共享盘敏感文件收割、批量可写共享排查。信号:内网枚举,网络发现,匿名/当前会话列共享,指定凭据。"
when-to-use: >-
  Use when enumerating SMB shares to find sensitive files or writable shares
  on internal hosts; provide a host or host file with optional credentials and
  recursively list or download share contents.
---

# smbmap

- Attack Category: C29 Internal Network Discovery and Enumeration
- Upstream Repository: https://github.com/ShawnDEvans/smbmap
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install smbmap
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `smbmap -H 10.0.0.5` | List shares anonymously / with the current session |
| `-u user -p pass -d corp -H ip` | Specify credentials |
| `-R SHARE --depth 3` | Recursively list directories |
| `-A '.conf|.yml|.xml'` | Search files by extension |
| `--upload path local SHARE/remote` | Upload |
| `--download` | Download |
| `-x 'whoami'` | Remote execution (x must be configured) |

## Attack Scenario Playbook

### Harvesting sensitive files from shares

```bash
smbmap -u svc -p Pass123 -d corp -H 10.0.0.5 -R DATA --depth 2 | grep -iE 'pass|secret|key|config'
```

### Bulk check for writable shares

```bash
smbmap -u user -p pass -d corp --host-file ips.txt | grep -E 'READ,WRITE|WRITE'
```

## Notes

More granular than crackmapexec for share enumeration; --download is efficient over a whole directory tree.
