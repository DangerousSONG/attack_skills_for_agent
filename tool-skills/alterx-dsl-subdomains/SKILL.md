---
name: alterx-dsl-subdomains
description: "alterx: generates new candidates from passive results. Signals: asset mapping, subdomain, generate candidates from known subdomains, directly specify target"
zh-signals: "alterx: 被动结果驱动的新候选生成。信号:资产测绘,子域名,基于已知子域生成候选,直接指定目标。"
when-to-use: >-
  Use when generating new subdomain candidates from passive enumeration
  results; feed known subdomains and pipe the enriched candidates into DNS
  resolution.
---

# alterx

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/projectdiscovery/alterx
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/projectdiscovery/alterx/cmd/alterx@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `-l known_subdomains.txt` | Generate candidates from known subdomains |
| `-list target.com` | Specify the target directly |
| `-enrich` | Enrich with a resolver |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Passive result-driven candidate generation

```bash
subfinder -d corp.com -silent | alterx -enrich | dnsx -silent -a
# Learns the pattern from known subdomains to create candidates such as api2/dev-v2 and resolves them
```

## Notes

The DSL permutation engine of the pd ecosystem; richer patterns than altdns, and best results when combined with known subdomains.
