---
name: crlfuzz-crlf-injection
description: "CRLFuzz: Tests response splitting via CRLF injection. Signals: web vulnerability, injection, single-target CRLF injection, batch."
zh-signals: "CRLFuzz: 响应拆分测试。信号:web漏洞,注入,单目标 CRLF 注入,批量。"
when-to-use: >-
  Use when testing a URL's parameters for CRLF injection and HTTP response
  splitting. Supports single targets, batch lists, and silent output.
---

# CRLFuzz

- Attack Category: C09 Web Exploitation (CRLF / HTTP Header Injection)
- Upstream Repository: https://github.com/dwisiswant0/crlfuzz
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/dwisiswant0/crlfuzz/cmd/crlfuzz@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `crlfuzz -u 'https://t.com/?url=x'` | Single-target CRLF injection |
| `-l urls.txt` | Batch |
| `-o out.txt` | Output |
| `-s` | Quiet mode |

## Attack Scenario Playbook

### Response Splitting Test

```bash
crlfuzz -u 'https://t.com/redirect?next=https://a.com'
# On a hit, inject a Set-Cookie / 302 Location header
```

## Notes

Written in Go, fast; injects CRLF (%0d%0a) into every URL parameter and detects response header reflection.
