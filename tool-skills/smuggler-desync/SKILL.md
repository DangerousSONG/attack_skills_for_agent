---
name: smuggler-desync
description: "Smuggler: frontend and CDN smuggling detection. Signals: web vulnerability, injection, HTTP request smuggling detection, detailed, deep mode."
zh-signals: "Smuggler: 前端/CDN 走私检测。信号:web漏洞,注入,HTTP 请求走私检测,详细,深入模式。"
when-to-use: "Use Smuggler when you suspect HTTP request smuggling or desynchronization between a frontend/CDN and backend, and need to detect CL.TE/TE.CL/TE.TE variants with ready-to-use PoC requests."
---

# Smuggler

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/defparam/smuggler
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/defparam/smuggler
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python smuggler.py -u https://t.com` | HTTP request smuggling detection |
| `-v 2` | Verbose |
| `-x` | Deep mode |
| `-m GET` | Method |
| `--no-color` | No colors |

## Attack Scenario Playbook

### Frontend/CDN Smuggling Detection

```bash
python smuggler.py -u https://target -v 2
# Tests CL.TE/TE.CL/TE.TE obfuscation and prints a full PoC request on a hit
```

## Notes

The benchmark for HTTP desync detection; on a hit, build smuggling requests from its PoC to bypass the frontend ACL and pivot into the internal network.
