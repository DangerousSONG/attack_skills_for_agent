---
name: doork-dork-scan
description: "doork: automated target dorking. Signals: web vulnerability, injection, custom dork."
zh-signals: "doork: 目标 dork 自动化。信号:web漏洞,注入,自定义 dork。"
when-to-use: >-
  Use when you need to automate Google dorking against a target domain to
  surface leaked files, admin panels, and exposed configurations. Accepts
  custom dork expressions and writes results to an output file.
---

# doork

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/AeonDave/doork
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/AeonDave/doork && cd doork
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python doork.py -t corp.com` | Google dork target scan |
| `-t target -g 'ext:sql'` | Custom dork |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Automated Target Dorking

```bash
python doork.py -t corp.com
# Automatically dork for leaked files/admin panels/configurations
```

## Notes

Google dork automation with preset queries for sensitive file types.
