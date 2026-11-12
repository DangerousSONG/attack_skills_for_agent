---
name: hakrawler-fast-crawler
description: "hakrawler quickly harvests site endpoints. Signals: asset mapping, subdomains, hakrawler, crawl depth 3, include subdomains."
zh-signals: "hakrawler: 站点端点快速收割。信号:资产测绘,子域名,hakrawler`,爬深 3 层,包含子域。"
when-to-use: "Use during asset mapping to quickly harvest URLs, endpoints, and JavaScript files from a site, optionally including subdomains. Requires a target URL and a crawl depth."
---

# hakrawler

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/hakluke/hakrawler
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/hakluke/hakrawler@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `echo https://target.com | hakrawler` | Crawl endpoints/forms/JS |
| `-d 3` | Crawl depth 3 |
| `-subs` | Include subdomains |
| `-u` | Show source URL |
| `-t 20` | Threads |
| `-insecure` | Ignore TLS errors |
| `-proxy http://127.0.0.1:8080` | Go through a proxy |

## Attack Scenario Playbook

### Fast Harvest of Site Endpoints

```bash
echo https://app.target.com | hakrawler -d 2 -subs | sort -u > endpoints.txt
grep -E '\?.*=' endpoints.txt > params.txt  # feed into a parameter wordlist brute force
```

## Notes

A fast crawler written in Go whose plain-text output suits pipelines; its form and JS discovery is useful input for a fuzzer.
