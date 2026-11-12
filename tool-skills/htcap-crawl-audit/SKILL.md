---
name: htcap-crawl-audit
description: "htcap fully crawls Ajax sites. Signals: web vulnerability, injection, crawl and store SQLite, vulnerability assessment, crawl depth."
zh-signals: "htcap: Ajax 站点全量爬取。信号:web漏洞,注入,爬取+存 SQLite,漏洞评估,爬深。"
when-to-use: >-
  Use when auditing modern Ajax-heavy web applications that client-side crawling
  misses; crawl the site, store results in SQLite, then run vulnerability
  assessment on the captured data.
---

# htcap

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/segment-srl/htcap
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/segment-srl/htcap && cd htcap
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python htcap.py -w urls.txt -o db.sqlite https://t.com` | Crawl + store in SQLite |
| `python htcap.py --assess db.sqlite` | Vulnerability assessment |
| `-x 3` | Crawl depth |
| `-p 20` | Concurrency |

## Attack Scenario Playbook

### Full Crawl of Ajax Sites

```bash
python htcap.py https://t.com -o t.sqlite
# Headless browser crawls the SPA and produces a vulnerability assessment database
```

## Notes

Crawler from segment, purpose-built for Ajax/JS-heavy sites, outputting structured queryable data.
