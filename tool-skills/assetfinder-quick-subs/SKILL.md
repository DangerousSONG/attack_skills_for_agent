---
name: assetfinder-quick-subs
description: "assetfinder: acts as the first stage in a recon pipeline. Signals: asset mapping, subdomain, list subdomains only, subdomains+related domains, quiet output for pipelines"
zh-signals: "assetfinder: 侦察流水线第一棒。信号:资产测绘,子域名,只列子域名,子域+关联域名,静默输出便于管道。"
when-to-use: >-
  Use when kicking off a subdomain recon pipeline and you need a fast, silent list of subdomains
  and related domains that pipes into other tools.
---

# assetfinder

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/tomnomnom/assetfinder
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/tomnomnom/assetfinder@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `assetfinder --subs-only target.com` | List subdomains only |
| `assetfinder target.com` | Subdomains + related domains |
| `--silent` | Quiet output for pipelines |

## Attack Scenario Playbook

### First Stage of the Recon Pipeline

```bash
assetfinder --subs-only corp.com | sort -u | tee subs.txt
subfinder -d corp.com -silent >> subs.txt && sort -u subs.txt -o subs.txt
```

## Notes

A lightweight tool by tomnomnom that runs fast; complements subfinder, dedupe and feed into dnsx.
