---
name: http2smugl-desync
description: "http2smugl detects HTTP/2 request smuggling. Signals: web vulnerability, injection, second obfuscation mode, inject smuggling prefix, report only exploitable targets."
zh-signals: "http2smugl: HTTP/2 走私检测。信号:web漏洞,注入,第二种混淆模式,注入走私前缀,只报可利用目标。"
when-to-use: >-
  Use when testing an HTTP/2 to HTTP/1.1 conversion layer for request smuggling via CL.TE or TE.CL desynchronization, with optional payload injection and vulnerable-only reporting.
---

# http2smugl

- Attack Category: C09 Web Exploitation (HTTP Request Smuggling)
- Upstream Repository: https://github.com/neex/http2smugl
- Upstream License: Unlicense (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/neex/http2smugl && cd http2smugl && pip install .
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `http2smugl -u 'https://t.com/' -t CL.TE` | HTTP/2→1.1 request smuggling detection |
| `-t TE.CL` | Second obfuscation mode |
| `-c 'x=1'` | Inject a smuggling prefix |
| `--vulnerable-only` | Report only exploitable targets |

## Attack Scenario Playbook

### HTTP/2 Smuggling Detection

```bash
http2smugl -u 'https://t.com/' -t CL.TE
# On a hit, craft a CL.TE prefix to smuggle an arbitrary request to the backend
```

## Notes

Focuses on the smuggling surface created during HTTP/2 to HTTP/1.1 conversion (CL.TE/TE.CL obfuscation).
