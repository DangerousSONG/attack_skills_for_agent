---
name: zmap-internet
description: "ZMap: Internet-scale fast measurement. Signals: port scan, nmap, single-port internet-wide scan, bandwidth limit, target count cap."
zh-signals: "ZMap: 互联网级快速测量。信号:端口扫描,nmap,单端口全网扫,带宽限制,目标数上限。"
when-to-use: >-
  Use when performing internet-wide single-port measurements at high speed and
  you need to control bandwidth and cap the target count.
---

# ZMap

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/zmap/zmap
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install zmap or build from source
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `zmap -p 443 10.0.0.0/8` | Single-port internet-wide scan |
| `-B 10M` | Bandwidth limit |
| `-n 100000` | Target count cap |
| `-o out.txt` | Output |
| `-r 10000` | Rate in pps |
| `--output-fields=sport,sip` | Fields |
| `-w whitelist.txt` | Allowlist |
| `-c 3` | Number of packets sent |

## Attack Scenario Playbook

### Internet-scale fast measurement

```bash
zmap -p 8443 -B 50M -n 1000000 -o vpn_gateways.txt
# Scans the entire internet on port 443 in 45 minutes; pair with zgrab2 for application-layer fingerprinting
```

## Notes

An academic-grade single-packet scanning engine; always confirm the authorization scope, the legal risk of misuse is extremely high.
