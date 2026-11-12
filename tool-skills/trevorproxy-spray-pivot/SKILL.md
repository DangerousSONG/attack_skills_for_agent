---
name: trevorproxy-spray-pivot
description: "TREVORproxy sprays from multiple source IPs. Signals: internal pivoting, tunneling, proxy-pool spraying, combinations, lists"
zh-signals: "TREVORproxy: 多源 IP 喷洒。信号:内网穿透,隧道,代理池喷洒,组合,列表。"
when-to-use: >-
  Use when you need to spray or pivot through multiple source IPs to avoid rate
  limiting and blend traffic during internal engagements.
---

# TREVORproxy

- Attack Category: C32 Tunneling and Internal Network Pivoting
- Upstream Repository: https://github.com/blacklanternsecurity/TREVORproxy
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install trevorproxy
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `trevorproxy -i eth0 -d target.com` | Proxy pool spraying |
| `-i eth0 -d d -u u.txt` | Combinations |
| `-l` | List |

## Attack Scenario Playbook

### Multi-Source IP Spraying

```bash
trevorproxy -i eth0 -d corp.com
# Rotate across multiple NIC IPs
```

## Notes

By Black Lantern, a multi-egress-IP proxy.
