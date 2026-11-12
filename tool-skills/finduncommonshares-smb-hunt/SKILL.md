---
name: finduncommonshares-smb-hunt
description: "pyFindUncommonShares finds sensitive data via uncommon shares. Signals: internal enumeration, network discovery, whole-network uncommon-share scan, specific share-name types, current-user readability checks."
zh-signals: "pyFindUncommonShares: 非常规共享找敏感数据。信号:内网枚举,网络发现,全网非常规共享扫描,特定共享名类型,顺带检查当前用户可读。"
when-to-use: "Use during internal network enumeration to find uncommon SMB shares across domain hosts that may contain scripts, backups, and credential files. Requires domain credentials and a DC IP to query."
---

# pyFindUncommonShares

- Attack Category: C29 AD and LDAP Enumeration
- Upstream Repository: https://github.com/p0dalirius/pyFindUncommonShares
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install git+https://github.com/p0dalirius/pyFindUncommonShares.git
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `finduncommonshares -u svc -p pass -d corp.local --dc-ip 10.0.0.1` | Whole-network uncommon share scan |
| `-t DFS-R` | Specific share name types |
| `--check-user-access` | Also check whether the current user can read them |
| `-v` | Verbose |

## Attack Scenario Playbook

### Finding sensitive data in uncommon shares

```bash
finduncommonshares -u svc -p pass -d corp.local --dc-ip 10.0.0.1
# Shares such as backup$/scripts$/transfer$ are goldmines holding password scripts and credential files
```

## Notes

By p0dalirius; scans every machine in the domain for non-default SMB shares and verifies access permissions.
