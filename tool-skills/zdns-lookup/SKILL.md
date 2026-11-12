---
name: zdns-lookup
description: "ZDNS: Million-scale DNS queries. Signals: asset mapping, subdomain, zdns A records, MX records, NS records."
zh-signals: "ZDNS: 百万级 DNS 查询。信号:资产测绘,子域名,zdns A`,MX 记录,NS 记录。"
when-to-use: >-
  Use when resolving millions of DNS records quickly for asset mapping; pipe
  names into A, MX, or NS lookups and write JSONL output for large-scale
  enumeration.
---

# ZDNS

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/zmap/zdns
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/zmap/zdns@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `echo corp.com | zdns A` | Bulk A record resolution |
| `zdns MX --name-servers 8.8.8.8` | MX records |
| `zdns NS` | NS records |
| `zdns A --output-file out.json` | JSON output |

## Attack Scenario Playbook

### Million-scale DNS queries

```bash
cat subs.txt | zdns A --threads 1000 -o resolved.jsonl
jq -r '.data.answers[]? | select(.type=="A") | .answer' resolved.jsonl
```

## Notes

The DNS engine from the ZMap team; a million queries complete in minutes, pushing further than dnsx.
