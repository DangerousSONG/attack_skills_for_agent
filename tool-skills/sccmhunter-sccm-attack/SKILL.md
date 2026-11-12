---
name: sccmhunter-sccm-attack
description: "SCCMHunter: Maps SCCM site assets. Signals: AD attack, domain penetration, view site details, ticket reuse mode, debug output."
zh-signals: "SCCMHunter: SCCM 站点资产测绘。信号:ad攻击,域渗透,查看站点详情,票据复用模式,调试输出。"
when-to-use: >-
  Use during AD attacks to map SCCM/MECM site infrastructure, including site
  servers, distribution points, and NAA credentials, before lateral movement.
---

# SCCMHunter

- Attack Category: C30 AD and Lateral Movement
- Upstream Repository: https://github.com/garrettfoster13/sccmhunter
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/garrettfoster13/sccmhunter && cd sccmhunter && pip install .
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `sccmhunter -u user -p pass -d corp.local http -ip 10.0.0.5` | MECM/SCCM site information enumeration |
| `sccmhunter -u user -p pass -d corp.local show -computer sccm01` | View site details |
| `sccmhunter ... smb -ip 10.0.0.5` | SCCM distribution point share enumeration |
| `-reuse-pwd 1` | Ticket reuse mode |
| `-debug` | Debug output |

## Attack Scenario Playbook

### SCCM Site Asset Mapping

```bash
sccmhunter -u lowpriv -p 'Pass1' -d corp.local http -ip 10.0.0.10
# Locate site servers → inspect DP/MP roles to pave the way for NAA credential theft
```

## Notes

Microsoft Configuration Manager (MECM/SCCM) attack tool: enumerates site information, DP contents, and NAA credentials via HTTP query / WMI / SMB.
