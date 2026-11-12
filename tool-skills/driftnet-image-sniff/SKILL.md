---
name: driftnet-image-sniff
description: "driftnet: LAN image sniffing. Signals: man-in-the-middle, MITM, image traffic sniffing, audio, save to disk."
zh-signals: "driftnet: 局域网图片嗅探。信号:中间人,mitm,图片流量嗅探,音频,落盘。"
when-to-use: >-
  Use when conducting authorized network sniffing or MITM testing on a LAN and you want
  to capture and display images or audio traffic passing through the interface.
---

# driftnet

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/deiv/driftnet
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install driftnet
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `driftnet -i eth0` | Image traffic sniffing |
| `-a` | Audio |
| `-d tmp/` | Save to disk |
| `-f` | Foreground |

## Attack Scenario Playbook

### LAN image sniffing

```bash
driftnet -i eth0
# Watch what images the target browses under ARP spoofing
```

## Notes

A network image sniffing tool.
