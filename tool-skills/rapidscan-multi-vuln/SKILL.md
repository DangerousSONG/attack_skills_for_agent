---
name: rapidscan-multi-vuln
description: "rapidscan: Aggregates results from multiple tools. Signals: web vulnerabilities, injection, one-click multi-tool orchestrated scan, SSL-only modules, exclude modules."
zh-signals: "rapidscan: 多工具结果聚合。信号:web漏洞,注入,一键多工具编排扫描,仅 SSL 模块,排除模块。"
when-to-use: "Use when you need a one-shot orchestrated web vulnerability scan of a target domain and want results from multiple tools such as nmap, nikto and wafw00f aggregated into a single report, optionally restricted to SSL modules or excluding noisy modules."
---

# rapidscan

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/skavngr/rapidscan
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/skavngr/rapidscan && cd rapidscan && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 rapidscan.py example.com` | One-shot multi-tool orchestrated scan |
| `-s ssl` | SSL modules only |
| `-e nikto` | Exclude module |
| `-o report` | Output |

## Attack Scenario Playbook

### Multi-Tool Result Aggregation

```bash
python3 rapidscan.py t.com
# Orchestrates 10+ tools such as nmap/nikto/wafw00f into a unified report
```

## Notes

Multi-tool orchestrated scanner, runs the common tools in one invocation and automatically summarizes the key findings.
