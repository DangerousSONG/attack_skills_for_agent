---
name: tinja-ssti
description: "TInjA detects SSTI across engines. Signals: web vulnerability, injection, SSTI detection, with Cookie, request file"
zh-signals: "TInjA: SSTI 全引擎检测。信号:web漏洞,注入,SSTI 检测,带 Cookie,请求文件。"
when-to-use: >-
  Use when testing web parameters or headers for SSTI and you need to detect
  the underlying template engine and obtain exploitable payloads.
---

# TInjA

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/Hackmanit/TInjA
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/Hackmanit/TInjA@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `tinja -u 'https://t.com/?name=x' -ac 'error'` | SSTI detection |
| `-u url -H 'Cookie: x'` | With Cookie |
| `-r req.txt` | Request file |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### SSTI detection across all engines

```bash
tinja -u 'https://t.com/greet?name=admin' -ac 'syntax error'
# Probe 30+ template engines and obtain exploitable payloads
```

## Notes

SSTI scanner by Hackmanit, with a cannibalization mode for deeper digging.
