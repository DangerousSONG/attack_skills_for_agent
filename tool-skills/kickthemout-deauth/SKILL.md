---
name: kickthemout-deauth
description: "kickthemout kicks LAN devices offline with ARP. Signals: MITM, mitm, LAN device disconnection, kick all."
zh-signals: "kickthemout: 内网设备 ARP 踢下线。信号:中间人,mitm,局域网设备踢下线,kick 全部。"
when-to-use: "Use kickthemout when you need to force LAN devices offline via ARP spoofing, for example to make them reconnect to a rogue hotspot during a wireless assessment."
---

# kickthemout

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/k4m4/kickthemout
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/k4m4/kickthemout && cd kickthemout && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 kickthemout.py` | Kick LAN devices offline |
| `-s` | Scan |
| `-k` | Kick all |

## Attack Scenario Playbook

### ARP kicking of LAN devices

```bash
python3 kickthemout.py
# Force a reconnect to a rogue hotspot
```

## Notes

Kicks devices offline via ARP spoofing.
