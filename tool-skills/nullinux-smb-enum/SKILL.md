---
name: nullinux-smb-enum
description: "All-in-one SMB enumeration on Linux. Signals: asset mapping, subdomains, SMB/RPC enumeration, share enumeration, user enumeration."
zh-signals: "Nullinux: Linux 上 SMB 枚举一把梭。信号:资产测绘,子域名,SMB/RPC 全枚举,共享枚举,用户枚举。"
when-to-use: >-
  Use when enumerating SMB/RPC on Linux against a host or network range to gather
  shares, users, groups, and RID information; supports quick, shares, and users
  modes.
---

# Nullinux

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/m8r0wn/nullinux
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/m8r0wn/nullinux && cd nullinux && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python nullinux.py 10.0.0.5` | Full SMB/RPC enumeration |
| `-shares` | Share enumeration |
| `-users` | User enumeration |
| `-quick` | Quick mode |

## Attack Scenario Playbook

### All-in-one SMB enumeration on Linux

```bash
python nullinux.py 10.0.0.0/24 -users -shares  # Domain users/shares/groups/RIDs all in one
```

## Notes

A modern Python rewrite of enum4linux; the output is tidy and easy for scripts to consume.
