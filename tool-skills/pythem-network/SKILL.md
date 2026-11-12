---
name: pythem-network
description: "PytheM: Integrated network penetration framework. Signals: man-in-the-middle, MITM, network attack framework, ARP spoofing, sniffing."
zh-signals: "PytheM: 网络渗透一体化。信号:中间人,mitm,网络攻击框架,ARP 欺骗,嗅探。"
when-to-use: >-
  Use when you need an integrated Python framework for local network attacks such as ARP spoofing, sniffing, DNS poisoning and service brute forcing.
---

# PytheM

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/m4n3dw0lf/PytheM
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/m4n3dw0lf/PytheM && cd PytheM && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 pythem.py -i eth0` | Network attack framework |
| `-i eth0 -arpspoof` | ARP spoofing |
| `-i eth0 - sniff` | Sniffing |
| `-i eth0 - brute ssh` | Brute force |

## Attack Scenario Playbook

### Integrated Network Penetration

```bash
python3 pythem.py -i eth0
# ARP / DNS / sniffing / brute force in one framework
```

## Notes

An all-in-one Python framework for network penetration testing.
