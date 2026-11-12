---
name: dnssearch-enum
description: "dnsSearch: lightweight fast subdomain brute-forcing. Signals: asset mapping, subdomain, resolver, threads."
zh-signals: "dnsSearch: 快速子域爆破轻量件。信号:资产测绘,子域名,resolver,线程。"
when-to-use: "Use dnsSearch when performing lightweight, low-resource subdomain brute-forcing for asset mapping, such as from a jump host, with custom resolvers and thread counts."
---

# dnsSearch

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/ptrrkssn/dnssearch
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/ptrrkssn/dnssearch && cd dnssearch && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `dnssearch -d corp.com -w wordlist.txt` | Subdomain brute force |
| `-r resolvers.txt` | resolver |
| `-t 20` | Threads |

## Attack Scenario Playbook

### Lightweight Fast Subdomain Brute-Forcer

```bash
dnssearch -d corp.com -w subs.txt -r resolvers.txt
```

## Notes

A small C tool with very low resource usage, ideal for running on a jump host.
