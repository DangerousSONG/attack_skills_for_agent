---
name: see-surf-ssrf
description: "See-SURF: crawling plus SSRF dual probing. Signals: web vulnerability, injection, crawl-based SSRF detection, OOB callback, concurrency."
zh-signals: "See-SURF: 爬取+SSRF 双探测。信号:web漏洞,注入,SSRF 爬取式检测,OOB 回调,并发。"
when-to-use: >-
  Use to crawl a web application and then probe all discovered URL parameters
  for SSRF, optionally using an OOB callback server.
---

# See-SURF

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/In3tinct/See-SURF
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/In3tinct/See-SURF && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 see-surf.py -u https://t.com` | Crawl-based SSRF detection |
| `-u url -b http://burp.collab` | OOB callback |
| `-c 20` | Concurrency |
| `-w urls.txt` | Batch |

## Attack Scenario Playbook

### Crawling plus SSRF dual probing

```bash
python3 see-surf.py -u https://t.com -b http://vps.oob.sh
# Crawl the whole site first, then probe the parameters for SSRF
```

## Notes

Crawls the target with Python3 and Selenium, then injects SSRF payloads into every URL parameter.
