---
name: dontgo403-bypass
description: "dontgo403: 403 endpoint bypass. Signals: web vulnerability, injection, 403 bypass testing, batch paths, request method rotation."
zh-signals: "dontgo403: 403 端点绕过。信号:web漏洞,注入,403 绕过测试,批量路径,请求方式轮换。"
when-to-use: >-
  Use when an endpoint returns 403 and you want to test bypass techniques such
  as path tricks, header spoofing, and method rotation. Supports batch paths
  and custom headers.
---

# dontgo403

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/ivan-sincek/dontgo403
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/ivan-sincek/dontgo403@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `dontgo403 -u https://t.com/admin` | 403 bypass testing |
| `-p paths.txt` | Batch paths |
| `-m 5` | Request method rotation |
| `-H 'Header: value'` | Custom headers |

## Attack Scenario Playbook

### 403 endpoint bypass

```bash
dontgo403 -u https://target/admin -p admin_paths.txt
# Auto rotation: trailing slash/../ bypass/IP header spoofing (X-Forwarded-For 127.0.0.1)/uppercase method/encoding
```

## Notes

Ships 40+ bypass technique templates; complements 4xx scanners (bypass-403 style tools).
