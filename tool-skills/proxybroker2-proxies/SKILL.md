---
name: proxybroker2-proxies
description: "Build public proxy pool. Signals: intranet tunneling, tunnel, public proxy discovery, proxy pool service, scraping."
zh-signals: "proxybroker2: 公共代理池构建。信号:内网穿透,隧道,公共代理发现,代理池服务,抓取。"
when-to-use: >-
  Use when you need to discover public HTTP/HTTPS/SOCKS proxies and run them as
  a local rotating proxy pool service for anonymized egress.
---

# proxybroker2

- Attack Category: C32 Tunneling and Internal Network Pivoting
- Upstream Repository: https://github.com/bluet/proxybroker2
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install proxybroker2
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `proxybroker find -t US -l 10` | Public proxy discovery |
| `serve -p 8888` | Proxy pool service |
| `grab -c US,UK` | Scrape |

## Attack Scenario Playbook

### Building a Public Proxy Pool

```bash
proxybroker find --types HTTP HTTPS -l 50
# Anonymous egress pool
```

## Notes

Public proxy discovery plus a pooled proxy service.
