---
name: subbrute-dns-spider
description: "SubBrute enumerates subdomains without dictionaries via meta queries. Signals: subdomain, domain enumeration, meta-query spider enumeration, small-dictionary quick scan, custom resolver"
zh-signals: "SubBrute: 免字典元查询枚举。信号:子域名,域名枚举,元查询蜘蛛枚举,小字典快扫,自定义 resolver。"
when-to-use: >-
  Use when enumerating subdomains without large dictionaries via meta-query
  spidering; run against a domain with optional small wordlist, custom
  resolvers, and thread count.
---

# SubBrute

- Attack Category: C02 Domain and DNS Reconnaissance
- Upstream Repository: https://github.com/TheRook/subbrute
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/TheRook/subbrute
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python subbrute.py target.com` | Meta-query spider enumeration |
| `-s subdomains.txt` | Small-dictionary quick scan |
| `-r resolvers.txt` | Custom resolvers |
| `-t 32` | Threads |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Dictionary-free meta-query enumeration

```bash
python subbrute.py corp.com
# Use open resolvers for meta queries to find subdomains without a large dictionary
```

## Notes

Its strengths are resolver rotation and meta queries, which bypass some DNS rate limits; pair it with massdns for even better results.
