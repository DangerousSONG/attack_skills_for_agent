---
name: stowaway-pivot
description: "Stowaway provides multi-layer internal network pivoting. Signals: internal pivoting, tunneling, agent listen, admin connection, key"
zh-signals: "Stowaway: 多层内网穿透。信号:内网穿透,隧道,agent 监听,admin 连接,密钥。"
when-to-use: >-
  Use when establishing multi-layer pivoting into an internal network through
  multiple agents with a SOCKS proxy.
---

# Stowaway

- Attack Category: C32 Tunneling and Internal Network Pivoting
- Upstream Repository: https://github.com/ph4ntonn/Stowaway
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/ph4ntonn/Stowaway && cd Stowaway && go build
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./stowaway_agent -l 9999` | Agent listener |
| `./stowaway_admin -c 10.0.0.5:9999` | Admin connection |
| `-s secret` | Key |
| `socks 5` | SOCKS proxy |

## Attack Scenario Playbook

### Multi-layer internal network pivoting

```bash
./stowaway_agent -l 9999 && ./stowaway_admin -c target:9999
# Multi-hop agent topology
```

## Notes

Go-based internal network pivoting framework, multi-hop agents plus SOCKS5.
