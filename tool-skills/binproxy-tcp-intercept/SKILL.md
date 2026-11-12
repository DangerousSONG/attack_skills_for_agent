---
name: binproxy-tcp-intercept
description: "BinProxy: intercepts binary protocols. Signals: man-in-the-middle, mitm, binary protocol MITM, SSL, debugging"
zh-signals: "BinProxy: 私有协议中间人。信号:中间人,mitm,二进制协议中间人,SSL,调试。"
when-to-use: >-
  Use when you need to intercept and inspect a binary protocol such as RDP or MSSQL during
  authorized MITM testing, with optional SSL and debugging support.
---

# BinProxy

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/nccgroup/BinProxy
- Upstream License: AGPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
gem install binproxy
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `binproxy -l 8080 -r 10.0.0.5:3389 -p rdp` | Binary protocol man-in-the-middle |
| `-l l -r r -p proto -s` | SSL |
| `-d` | Debug |

## Attack Scenario Playbook

### Proprietary Protocol Man-in-the-Middle

```bash
binproxy -l 8080 -r 10.0.0.5:1433 -p tds
# from NCC, intercepts RDP/MSSQL and more
```

## Notes

From NCC; a man-in-the-middle proxy for any binary protocol.
