---
name: punter-multi-source
description: "Punter: Aggregates passive subdomains from multiple sources. Signals: asset mapping, subdomains, passive subdomain collection, includes active validation."
zh-signals: "Punter: 多源被动子域聚合。信号:资产测绘,子域名,被动子域收集,含主动验证。"
when-to-use: >-
  Use for initial asset mapping to aggregate passive subdomains from multiple
  free sources, optionally with active validation.
---

# Punter

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/nethunteros/punter
- Upstream License: Unlicense (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/nethunteros/punter && cd punter && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python punter.py -t target.com` | Passive subdomain collection |
| `-a` | Includes active validation |

## Attack Scenario Playbook

### Multi-Source Passive Subdomain Aggregation

```bash
python punter.py -t corp.com  # Aggregate DNSDumpster/WhoisXML/certificate transparency
```

## Notes

Aggregates multiple sources without an API key; good for the first-pass asset inventory.
