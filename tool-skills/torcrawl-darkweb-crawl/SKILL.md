---
name: torcrawl-darkweb-crawl
description: "TorCrawl structurally extracts dark-web sites. Signals: web vulnerability, injection, dark-web site crawl, crawl links, email extraction"
zh-signals: "TorCrawl: 暗网站点结构化提取。信号:web漏洞,注入,暗网站点爬取,爬取链接,提取邮箱。"
when-to-use: >-
  Use during dark-web OSINT when you need to crawl .onion sites, follow links,
  and extract emails or other structured data through Tor.
---

# TorCrawl

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/MikeMeliz/TorCrawl.py
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/MikeMeliz/TorCrawl.py && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 torcrawl.py -u http://target.onion` | Dark-web site crawl |
| `-u url -c` | Crawl links |
| `-u url -e` | Extract emails |
| `-d 2` | Depth |

## Attack Scenario Playbook

### Structured extraction of dark-web sites

```bash
python3 torcrawl.py -u http://leak.onion -e -d 3
# Bulk extraction from dark-web data leak sites
```

## Notes

A Tor network crawler that automatically goes through the Tor proxy to crawl .onion sites.
