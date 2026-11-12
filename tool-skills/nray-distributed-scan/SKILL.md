---
name: nray-distributed-scan
description: "Massive-scale port scanning. Signals: port scanning, nmap, distributed port scanning, rate, JSON output."
zh-signals: "nray: 超大规模端口扫描。信号:端口扫描,nmap,分布式端口扫描,速率,JSON 输出。"
when-to-use: >-
  Use when you need to port scan very large networks such as a /8 quickly with
  a distributed, event-driven scanner, and export the results as JSON.
---

# nray

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/nray-scanner/nray
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/nray-scanner/nray@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `nray -targets 10.0.0.0/24 -p 1-10000` | Distributed port scanning |
| `-targets cidr -rate 5000` | Rate |
| `-o out.json` | JSON output |
| `-workers 100` | Distributed nodes |

## Attack Scenario Playbook

### Massive-scale port scanning

```bash
nray -targets 10.0.0.0/8 -p top1000 -rate 10000
# Distributed architecture, an order of magnitude faster than nmap
```

## Notes

Event-driven port scanner with distributed support, built for high-volume scanning.
