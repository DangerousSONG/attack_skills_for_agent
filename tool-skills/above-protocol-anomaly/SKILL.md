---
name: above-protocol-anomaly
description: "Above: detects internal protocol-layer attacks. Signals: man-in-the-middle, mitm, protocol anomaly detection, ARP spoofing, PCAP analysis"
zh-signals: "Above: 内网协议层攻击检测。信号:中间人,mitm,协议异常检测,ARP 欺骗,PCAP 分析。"
when-to-use: >-
  Use when detecting protocol-layer attacks on an internal network, such as
  MITM or ARP spoofing anomalies, or analyzing captured PCAP traffic.
---

# Above

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/caster0x00/Above
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/caster0x00/Above && cd Above
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 above.py -i eth0 -F` | Protocol anomaly detection |
| `-i eth0 -d` | ARP spoofing |
| `-i eth0 -p` | PCAP analysis |

## Attack Scenario Playbook

### Internal Protocol-Layer Attack Detection

```bash
python3 above.py -i eth0 -d
# Capture anomalous protocol behavior (MITM/scanning)
```

## Notes

Protocol-layer anomaly detection to uncover internal network attack behavior.
