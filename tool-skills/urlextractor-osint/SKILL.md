---
name: urlextractor-osint
description: "URLextractor: Target URL intelligence aggregation. Signals: web vulnerabilities, injection, target OSINT extraction, include subdomains, with port scan."
zh-signals: "URLextractor: 目标 URL 情报聚合。信号:web漏洞,注入,目标 OSINT 提取,包含子域,含端口扫描。"
when-to-use: >-
  Use when you need OSINT URL and IP intelligence for a target domain as a
  starting point for a web assessment. Can include subdomains and port
  scanning.
---

# URLextractor

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/eschultze/URLextractor
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/eschultze/URLextractor && cd URLextractor
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./extractor.sh t.com` | Target OSINT extraction |
| `-d t.com -s` | Include subdomains |
| `-d t.com -p` | Include port scanning |

## Attack Scenario Playbook

### Target URL intelligence aggregation

```bash
./extractor.sh corp.com
# Collects URLs, IPs, and the tech stack from multiple sources
```

## Notes

Multi-source OSINT URL collection with technology stack identification.
