---
name: ike-scan-vpn-enum
description: "ike-scan probes VPN gateways and cracks PSKs. Signals: port scan, nmap, IKE service discovery and fingerprinting, readable multiline output."
zh-signals: "ike-scan: VPN 网关探测+PSK 破解。信号:端口扫描,nmap,IKE 服务发现+指纹,多行输出(易读)。"
when-to-use: >-
  Use when enumerating IPsec/IKE VPN gateways for service fingerprinting and
  capturing aggressive-mode PSK hashes for offline cracking.
---

# ike-scan

- Attack Category: C42 Network Service Enumeration
- Upstream Repository: https://github.com/royhills/ike-scan
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install ike-scan
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `ike-scan 10.0.0.1` | IKE service discovery and fingerprinting |
| `-M` | Multiline output (easy to read) |
| `-A` | Aggressive mode group name enumeration |
| `-P` | PSK capture (crack with hashcat -m 5400) |
| `-n payload.txt` | Custom transform |

## Attack Scenario Playbook

### VPN Gateway Probing and PSK Cracking

```bash
ike-scan -M -A 10.0.0.1
# Outputs the IKE fingerprint plus AGGRESSIVE mode handshake hashes, crack the PSK with hashcat -m 5400
```

## Notes

The standard tool for IPsec/IKE VPN probing, capturing PSK hashes in aggressive mode for offline cracking.
