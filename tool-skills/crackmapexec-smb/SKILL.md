---
name: crackmapexec-smb
description: "CrackMapExec / CME: Provides fast domain information over CIDR ranges. Signals: AD attack, domain penetration, SMB protocol alive enumeration, list SMB shares, remote hash extraction."
zh-signals: "CrackMapExec / CME: CIDR 级域内信息速览。信号:ad攻击,域渗透,SMB 协议枚举存活,列 SMB 共享,远程抓取哈希。"
when-to-use: >-
  Use when enumerating a domain over a CIDR range and you need to check SMB
  liveness, list shares and extract hashes remotely.
---

# CrackMapExec / CME

- Attack Category: C30 AD Domain Penetration and Domain Controller Attacks
- Upstream Repository: https://github.com/byt3bl33d3r/CrackMapExec
- Upstream License: BSD-2-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install crackmapexec (project archived, NetExec recommended for production)
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `crackmapexec smb 10.0.0.0/24` | Enumerate live hosts over SMB |
| `-u user -p pass --shares` | List SMB shares |
| `--sam / --lsa / --ntds` | Extract hashes remotely |
| `-M mimikatz` | Module execution |
| `--local-auth` | Local auth bypasses domain policy |

## Attack Scenario Playbook

### Fast CIDR-Range Overview of In-Domain Information

```bash
crackmapexec smb 10.0.0.0/24 -u svc -p Pass123
# Prints a table of hostnames/domains/signing status/OS
```

## Notes

Archived but still preinstalled in many environments; use NetExec in new environments, the syntax is nearly identical. This skill exists for compatibility with legacy environments.
