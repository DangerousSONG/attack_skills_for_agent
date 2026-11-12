---
name: proxify-multiproxy
description: "Multi-protocol proxy forwarding. Signals: intranet tunneling, tunnel, multi-level proxy, SOCKS5, traffic capture to disk."
zh-signals: "proxify: 多协议代理转发。信号:内网穿透,隧道,起多级代理,SOCKS5,流量落盘。"
when-to-use: >-
  Use when you need a multi-protocol HTTP/SOCKS5 proxy for pivoting, multi-level proxying and capturing traffic to disk during internal assessments.
---

# proxify

- Attack Category: C32 Tunneling and Internal Network Pivoting
- Upstream Repository: https://github.com/projectdiscovery/proxify
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/projectdiscovery/proxify@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `proxify -http-addr 0.0.0.0:8888` | Start a multi-level proxy |
| `-socks5-addr 0.0.0.0:9050` | SOCKS5 |
| `-output out/` | Write traffic to disk |

## Attack Scenario Playbook

### Multi-Protocol Proxy Forwarding

```bash
proxify -http-addr 127.0.0.1:8080
# HTTP/SOCKS5 conversion + TLS interception
```

## Notes

By ProjectDiscovery, a multi-purpose proxy tool.
