---
name: mitmap-ap-mitm
description: "mitmAP: Malicious hotspot phishing. Signals: man-in-the-middle, MITM, phishing hotspot+MITM, SSLStrip."
zh-signals: "mitmAP: 恶意热点钓鱼。信号:中间人,mitm,钓鱼热点+中间人,SSLStrip。"
when-to-use: >-
  Use when performing an authorized wireless MITM by standing up a rogue hotspot
  with a captive portal to harvest credentials.
---

# mitmAP

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/xdavidhu/mitmAP
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/xdavidhu/mitmAP && cd mitmAP
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 mitmAP.py -i wlan0 -t eth0` | Phishing hotspot + MITM |
| `-i in -t out -p` | SSLStrip |
| `-s` | SSLStrip2 |

## Attack Scenario Playbook

### Malicious Hotspot Phishing

```bash
python3 mitmAP.py -i wlan0 -t eth0
# forced captive portal + credential harvesting
```

## Notes

Malicious WiFi hotspot man-in-the-middle tool (requires a wireless adapter).
