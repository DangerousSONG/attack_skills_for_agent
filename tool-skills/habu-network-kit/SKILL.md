---
name: habu-network-kit
description: "habu is a network-layer Swiss Army toolkit. Signals: port scanning, nmap, IP information, ARP scanning, TCP flag probing."
zh-signals: "habu: 网络层 Swiss Army。信号:端口扫描,nmap,IP 信息,ARP 扫描,TCP 标志探测。"
when-to-use: >-
  Use when you need quick network-layer probing during recon, such as ARP discovery,
  IP information lookup, TCP flag probing or connectivity tests.
---

# habu

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/portantier/habu
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install habu
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `habu.ip -t t.com` | IP information |
| `habu.arp -i eth0` | ARP scanning |
| `habu.tcpflags -t 10.0.0.5` | TCP flag probing |
| `habu.contest` | Connectivity test |
| `habu.land -t ip` | LAND attack |

## Attack Scenario Playbook

### Network-Layer Swiss Army

```bash
habu.arp -i eth0 && habu.tcpflags -t 10.0.0.5
# ARP discovery + firewall identification
```

## Notes

Python network toolset with 100+ commands, a helper for network-layer penetration testing.
