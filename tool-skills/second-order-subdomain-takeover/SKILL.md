---
name: second-order-subdomain-takeover
description: "Second-order: batch subdomain takeover scanning. Signals: web vulnerability, injection, subdomain takeover detection, specified cloud service."
zh-signals: "second-order: 子域接管批量扫描。信号:web漏洞,注入,子域接管检测,指定云服务。"
when-to-use: >-
  Use when checking a list of subdomains for dangling DNS records and subdomain
  takeover across supported cloud providers.
---

# second-order

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/mhmdiaa/second-order
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/mhmdiaa/second-order@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `second-order -t https://t.com -w wordlist.txt` | Subdomain takeover detection |
| `-t url -c amazon,azure` | Specified cloud services |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Batch Subdomain Takeover Scanning

```bash
second-order -t subs.txt -w providers.txt
#  Dangling CNAME detection across 20+ cloud providers
```

## Notes

Scans for subdomain takeover, detecting dangling DNS records.
