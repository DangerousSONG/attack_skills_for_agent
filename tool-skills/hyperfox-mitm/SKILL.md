---
name: hyperfox-mitm
description: "Hyperfox performs MITM analysis of HTTP traffic. Signals: MITM, mitm, transparent proxy, traffic capture to disk."
zh-signals: "Hyperfox: HTTP 流量中间人分析。信号:中间人,mitm,透明代理,流量落盘。"
when-to-use: "Use when you need to intercept, record, and tamper HTTP/HTTPS traffic on a network as a transparent MITM proxy."
---

# Hyperfox

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/xiam/hyperfox
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/xiam/hyperfox@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `hyperfox -p 8080 -c cert.pem -k key.pem` | HTTP/HTTPS man-in-the-middle |
| `-p port -s` | Transparent proxy |
| `-o out/` | Write traffic to disk |

## Attack Scenario Playbook

### HTTP traffic man-in-the-middle analysis

```bash
hyperfox -p 8080 -c fake.crt -k fake.key
# Log and tamper with HTTP requests
```

## Notes

Go man-in-the-middle proxy with traffic recording and real-time tampering.
