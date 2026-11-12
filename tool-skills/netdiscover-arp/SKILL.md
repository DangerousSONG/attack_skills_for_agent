---
name: netdiscover-arp
description: "Netdiscover: Layer 2 alive discovery bypassing ping blocks. Signals: internal network enumeration, network discovery, ARP alive scan, specified interface, passive mode."
zh-signals: "Netdiscover: 二层存活发现(绕过禁 ping)。信号:内网枚举,网络发现,ARP 存活扫描,指定网卡,被动模式。"
when-to-use: "Use on a local segment when ICMP is blocked, discovering live hosts via ARP in active or passive mode."
---

# Netdiscover

- Attack Category: C29 Internal Network Discovery and Enumeration
- Upstream Repository: https://github.com/netdiscover-scanner/netdiscover
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install netdiscover
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `netdiscover -r 10.0.0.0/24` | ARP alive scan |
| `-i eth0` | Specify the network interface |
| `-p` | Passive mode |
| `-c 3` | Number of packets sent |

## Attack Scenario Playbook

### Layer 2 alive discovery (bypassing blocked ping)

```bash
netdiscover -r 10.0.0.0/16 -i eth0
# Probing at the ARP layer, unaffected by fully blocked firewalls/ICMP
```

## Notes

ARP discovery is the most reliable low-level liveness check in an internal network; passive mode (-p) sends no packets.
