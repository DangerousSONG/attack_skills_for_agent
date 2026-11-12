---
name: sipvicious-sip
description: "SIPVicious: internal VoIP pentesting. Signals: port scan, nmap, SIP device discovery, extension enumeration, SIP brute force."
zh-signals: "SIPVicious: VoIP 内网渗透。信号:端口扫描,nmap,SIP 设备发现,分机枚举,SIP 爆破。"
when-to-use: >-
  Use during internal VoIP or network reconnaissance to discover SIP devices,
  enumerate extensions, and brute-force SIP credentials.
---

# SIPVicious

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/EnableSecurity/sipvicious
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install sipvicious
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `svmap 10.0.0.0/24` | SIP device discovery |
| `svwar -m INVITE 10.0.0.5` | Extension enumeration |
| `svcrack -u 100 -d wordlist.txt 10.0.0.5` | SIP brute force |
| `svreport -t onlinehosts` | Report |

## Attack Scenario Playbook

### Internal VoIP Penetration Testing

```bash
svmap 10.0.0.0/24 && svwar -m INVITE 10.0.0.5
# Discovery + enumeration + brute force
```

## Notes

By EnableSecurity, the standard tool for VoIP security testing.
