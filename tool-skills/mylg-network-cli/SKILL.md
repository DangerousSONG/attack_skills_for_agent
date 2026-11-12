---
name: mylg-network-cli
description: "mylg: Swiss-army-knife network diagnostics. Signals: port scanning, nmap, comprehensive network scan, traceroute, DNS query."
zh-signals: "mylg: 瑞士军刀式网络诊断。信号:端口扫描,nmap,综合网络扫描,路由跟踪,DNS 查询。"
when-to-use: >-
  Use when performing quick network diagnostics or discovery, combining ping, traceroute, DNS, WHOIS and port scanning in a single Swiss-army-knife CLI.
---

# mylg

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/mehrdadrad/mylg
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/mehrdadrad/mylg@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `mylg scan 10.0.0.0/24` | Comprehensive network scan |
| `mylg trace 8.8.8.8` | Traceroute |
| `mylg dns t.com` | DNS query |
| `mylg whois t.com` | WHOIS |

## Attack Scenario Playbook

### Swiss-army-knife network diagnostics

```bash
mylg scan 10.0.0.0/24 --ping
# All-in-one scan and ping
```

## Notes

Network engineer toolkit combining ping, trace, dns, scan and whois.
