---
name: domained-multi-enum
description: "Domained: multi-tool orchestrated subdomain collection. Signals: asset mapping, subdomain, passive plus active subdomains, brute force only, active only."
zh-signals: "Domained: 多工具编排子域收集。信号:资产测绘,子域名,被动+主动子域,仅爆破,仅主动。"
when-to-use: >-
  Use when collecting subdomains with multiple orchestrated tools, combining
  passive and active sources or brute-force alone.
---

# Domained

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/TypeError/domained
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/TypeError/domained && cd domained && python domained.py -i target.com -p
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python domained.py -i target.com -p` | Passive plus active subdomains |
| `-b` | Brute force only |
| `-a` | Active only |

## Attack Scenario Playbook

### Multi-tool orchestrated subdomain collection

```bash
python domained.py -i corp.com -p  # Calls sublist3r/enumall/subfinder/amass and merges the results
```

## Notes

One-shot orchestration of multiple subdomain tools with deduplication, so you do not have to build the pipeline yourself.
