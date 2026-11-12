---
name: dublin-traceroute-nat
description: "dublin-traceroute: NAT path mapping. Signals: port scanning, nmap, JSON, readable."
zh-signals: "dublin-traceroute: NAT 路径测绘。信号:端口扫描,nmap,JSON,可读。"
when-to-use: "Use when mapping network paths through NAT devices where standard traceroute fails to reveal per-flow load balancing."
---

# dublin-traceroute

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/insomniacslk/dublin-traceroute
- Upstream License: BSD-2-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install dublin-traceroute
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `dublin-traceroute 8.8.8.8` | NAT-aware traceroute |
| `-o out.json` | JSON |
| `--indent` | Readable |

## Attack Scenario Playbook

### NAT Path Mapping

```bash
dublin-traceroute corp.com
# Identify NAT devices + multiple paths
```

## Notes

By insomniacslk, a NAT-aware traceroute.
