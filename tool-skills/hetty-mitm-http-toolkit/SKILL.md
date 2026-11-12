---
name: hetty-mitm-http-toolkit
description: "hetty intercepts and modifies HTTPS traffic for testing. Signals: MITM, mitm, upstream proxy chaining, domain filtering, noise reduction."
zh-signals: "hetty: HTTPS 流量拦截改包测试。信号:中间人,mitm,链上游代理,限定拦截域名避免噪音。"
when-to-use: "Use when you need a lightweight Burp Suite alternative to intercept, inspect, replay, and modify HTTPS traffic during manual web testing. Requires installing the hetty CA certificate on the client and configuring proxy scope to limit noise."
---

# hetty

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/dstotijn/hetty
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/dstotijn/hetty/cmd/hetty@latest or download the release binary
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `hetty --cert-store ./certs` | Start the MITM proxy (:8080 + admin UI :31337) |
| `--proxy http://upstream:3128` | Chain an upstream proxy |
| `scope configuration` | Restrict intercepted domains to reduce noise |

## Attack Scenario Playbook

### HTTPS traffic interception and modification for testing

```bash
hetty --cert-store ./certs
# Install the hetty CA certificate on the browser/phone, proxy to :8080, then intercept, replay and modify in the web UI
```

## Notes

Go-based Burp alternative with low resource usage, suitable for running a long-lived proxy; certificates stored in ./certs can be reused.
