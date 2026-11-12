---
name: macchanger-spoof
description: "macchanger: Spoof MAC addresses. Signals: man-in-the-middle, MITM, random MAC, specified MAC, view."
zh-signals: "macchanger: MAC 地址伪装。信号:中间人,mitm,随机 MAC,指定 MAC,查看。"
when-to-use: >-
  Use when you need to change a NIC's MAC address to bypass MAC filtering or
  blend into a network for MITM and sniffing.
---

# macchanger

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/alobbs/macchanger
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install macchanger
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `macchanger -r eth0` | Random MAC |
| `-m 00:11:22:33:44:55` | Specified MAC |
| `-s eth0` | View |

## Attack Scenario Playbook

### MAC address spoofing

```bash
macchanger -r wlan0
# Bypass MAC filtering
```

## Notes

MAC address modification tool.
