---
name: xsstrike-xss
description: "XSStrike: Intelligent XSS detection. Signals: web vulnerability, injection, automatic XSS detection, site crawl scan, POST."
zh-signals: "XSStrike: 智能 XSS 打点。信号:web漏洞,注入,自动 XSS 检测,爬站扫,POST。"
when-to-use: >-
  Use when testing web endpoints for XSS with context-aware payload generation, including crawl mode, POST parameters and header injection.
---

# XSStrike

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/s0md3v/XSStrike
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/s0md3v/XSStrike && cd XSStrike && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python xsstrike.py -u 'https://t.com/search?q=test'` | Automatic XSS detection |
| `--crawl` | Crawl and scan the site |
| `--data 'q=1'` | POST |
| `--headers` | Inject into headers |
| `-t 5` | Threads |
| `--file-log` | Save results |
| `--path` | Path-based XSS |
| `--fuzzer` | Fuzz mode |

## Attack Scenario Playbook

### Intelligent XSS Detection

```bash
python xsstrike.py -u 'https://target/search?q=hello' --crawl
# 7 built-in parsers generate context-aware payloads, with a higher success rate than generic scanners
```

## Notes

Payloads are generated dynamically from the reflection context (not wordlist-based); crawl mode suits bulk triage of assets.
