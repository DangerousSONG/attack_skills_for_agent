---
name: ppfuzz-prototype-pollution
description: "Prototype pollution detection for JavaScript sites. Signals: web vulnerability, injection, batch, concurrency 30, JSON output."
zh-signals: "ppfuzz: JS 站原型链污染探测。信号:web漏洞,注入,批量,并发 30,JSON 输出。"
when-to-use: "Use when testing JavaScript-heavy web applications for client-side prototype pollution gadgets, scanning single URLs or batches with headless Chrome and JSON output."
---

# ppfuzz

- Attack Category: C09 Web Exploitation (Prototype Pollution)
- Upstream Repository: https://github.com/dwisiswant0/ppfuzz
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/dwisiswant0/ppfuzz/cmd/ppfuzz@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `ppfuzz -u 'https://t.com'` | Single-URL prototype pollution scan |
| `-l urls.txt` | Batch |
| `-c 30` | Concurrency 30 |
| `-o out.json` | JSON output |
| `-X POST -d 'a=b'` | POST mode |

## Attack Scenario Playbook

### Prototype pollution probing on JavaScript sites

```bash
ppfuzz -u 'https://app.t.com' -c 50 -o pp.json
# Manually verify after a hit: https://t.com/?__proto__[polluted]=yes
```

## Notes

Built on headless Chrome; scans JavaScript libraries for prototype pollution points (gadget detection).
