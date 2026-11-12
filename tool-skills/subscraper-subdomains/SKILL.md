---
name: subscraper-subdomains
description: "SubScraper mines subdomains from DNS records. Signals: asset mapping, subdomain, passive+DNS record enumeration, DNS record parsing"
zh-signals: "SubScraper: DNS 记录深挖子域。信号:资产测绘,子域名,被动+DNS 记录枚举,DNS 记录解析。"
when-to-use: >-
  Use during asset mapping to enumerate subdomains passively and by parsing DNS
  records such as A and CNAME, with configurable threads.
---

# SubScraper

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/m8sec/subscraper
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install subscraper
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `subscraper target.com` | Passive + DNS record enumeration |
| `-r` | DNS record parsing |
| `-o subs.txt` | Output |
| `-t 30` | Threads |

## Attack Scenario Playbook

### Mining Subdomains from DNS Records

```bash
subscraper corp.com -r -o subs.txt  # Correlate subdomains from MX/NS/SPF/CNAME records
```

## Notes

Its distinguishing feature is correlating DNS records rather than relying on a pure wordlist; it complements certificate transparency.
