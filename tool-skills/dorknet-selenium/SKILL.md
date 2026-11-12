---
name: dorknet-selenium
description: "DorkNet: dorking for anti-scraping scenarios. Signals: web vulnerability, injection, detailed, output URLs only."
zh-signals: "DorkNet: 反爬场景 dork。信号:web漏洞,注入,详细,仅输出 URL。"
when-to-use: >-
  Use for search-engine dorking when plain HTTP requests are blocked by
  anti-scraping, driving the queries through Selenium.
---

# DorkNet

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/NullArray/DorkNet
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/NullArray/DorkNet && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python DorkNet.py -d 'inurl:admin.php' -l results.txt` | Run dorks through Selenium |
| `-d dork -v` | Verbose |
| `-o` | Output URLs only |

## Attack Scenario Playbook

### Dorking against anti-scraping defenses

```bash
python DorkNet.py -d 'site:t.com ext:log'
# Driven by Selenium to bypass simple Google anti-scraping
```

## Notes

Selenium-driven dorking tool, well suited to cases where plain HTTP requests get blocked.
