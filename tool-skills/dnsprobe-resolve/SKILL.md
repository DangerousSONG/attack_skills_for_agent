---
name: dnsprobe-resolve
description: "dnsprobe: bulk subdomain resolution. Signals: subdomain, domain enumeration, dnsprobe, record types."
zh-signals: "dnsprobe: 子域批量解析。信号:子域名,域名枚举,dnsprobe`,记录类型。"
when-to-use: "Use when you have a list of candidate subdomains and need to resolve them in bulk, keeping only live domains; supports selecting record types and output files."
---

# dnsprobe

- Attack Category: C02 Domain and DNS Reconnaissance
- Upstream Repository: https://github.com/projectdiscovery/dnsprobe
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/projectdiscovery/dnsprobe@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `cat subs.txt | dnsprobe` | Bulk DNS resolution |
| `-r A,AAAA,CNAME` | Record types |
| `-o out.txt` | Output |
| `-t 5` | Timeout |

## Attack Scenario Playbook

### Bulk subdomain resolution

```bash
cat subs.txt | dnsprobe -r A -o resolved.txt
# Keeps only live domains
```

## Notes

From ProjectDiscovery; bulk DNS resolution (the predecessor component of httpx).
