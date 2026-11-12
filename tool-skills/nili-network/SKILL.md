---
name: nili-network
description: "nili: Combined scanning and MITM. Signals: port scanning, nmap, network scanning+MITM, sniffing, ARP spoofing."
zh-signals: "nili: 扫描+MITM 一体。信号:端口扫描,nmap,网络扫描+中间人,嗅探,ARP 欺骗。"
when-to-use: "Use nili when you need a single lightweight tool to scan an internal network and then perform MITM activities such as sniffing or ARP spoofing against the discovered hosts."
---

# nili

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/niloofarkheirkhah/nili
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/niloofarkheirkhah/nili && cd nili
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 nili.py -t 10.0.0.0/24` | Network scanning + man-in-the-middle |
| `-t cidr -s` | Sniffing |
| `-t cidr -d` | ARP spoofing |

## Attack Scenario Playbook

### Scanning + MITM in one tool

```bash
python3 nili.py -t 10.0.0.0/24 -s
# Lightweight internal network tool
```

## Notes

A combined network scanning and man-in-the-middle tool.
