---
name: arjun-param-discovery
description: "Arjun: mines hidden parameters to expand attack surface. Signals: web scan, vulnerability scan, HTTP parameter discovery, POST methods, rate limiting to avoid WAF"
zh-signals: "Arjun: 隐藏参数挖掘→扩大攻击面。信号:web扫描,漏洞扫描,HTTP 参数发现,POST 方法,降低速率防 WAF。"
when-to-use: "Use Arjun when mapping a web application's hidden HTTP parameters to expand the attack surface, including POST endpoints, with rate limiting to avoid WAF detection."
---

# Arjun

- Attack Category: C41 Web Vulnerability Scanning and Validation
- Upstream Repository: https://github.com/s0md3v/Arjun
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install arjun
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `arjun -u https://api.target.com/endpoint` | HTTP parameter discovery |
| `-m POST` | POST method |
| `--stable` | Lower the rate to avoid WAF detection |
| `-t 20` | Threads |
| `-oJ out.json` | JSON output |

## Attack Scenario Playbook

### Hidden Parameter Mining → Expand the Attack Surface

```bash
arjun -u https://api.target.com/v1/users -m GET,POST -oJ params.json
# Hand the discovered admin/debug/id parameters over to ffuf for deeper testing
```

## Notes

Detects undocumented parameters based on response differences (length/status code); it is common to first scrape parameter names from JS files and then run it.
