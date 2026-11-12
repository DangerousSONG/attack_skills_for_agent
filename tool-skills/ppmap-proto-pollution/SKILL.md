---
name: ppmap-proto-pollution
description: "Prototype pollution verification. Signals: web vulnerability, injection, prototype pollution detection, OOB callback."
zh-signals: "ppmap: 原型链污染验证。信号:web漏洞,注入,原型链污染检测,带 OOB 回调。"
when-to-use: "Use to detect and verify client-side prototype pollution, optionally with an OOB callback to confirm exploitability."
---

# ppmap

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/kleiton0x00/ppmap
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/kleiton0x00/ppmap && cd ppmap && go build
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./ppmap 'https://t.com/?__proto__[test]=test'` | Prototype pollution detection |
| `-c 'http://10.0.0.5:4444'` | With OOB callback |

## Attack Scenario Playbook

### Prototype Pollution Verification

```bash
./ppmap 'https://t.com/search?q=x'
# Automatically traverses common gadgets
```

## Notes

A prototype pollution scanner written in Go; detects gadgets and verifies them automatically.
