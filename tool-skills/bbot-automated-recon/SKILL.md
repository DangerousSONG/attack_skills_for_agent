---
name: bbot-automated-recon
description: "BBOT: performs one-stop full asset mapping, passive first then active gap filling. Signals: asset mapping, subdomain, subdomain enumeration preset, passive-only no target contact"
zh-signals: "BBOT: 全域资产测绘一站式、被动前置→主动补漏。信号:资产测绘,子域名,子域名枚举 preset,纯被动(不触目标)。"
when-to-use: >-
  Use when running one-stop asset mapping with passive-first and active
  gap-filling presets; choose presets such as subdomain-enum, web-basic, or
  cloud-enum, and use passive mode to avoid touching the target.
---

# BBOT

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/blacklanternsecurity/bbot
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install bbot
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `bbot -t target.com -p subdomain-enum` | Subdomain enumeration preset |
| `-p web-basic` | Web fingerprinting + screenshot basic preset |
| `-p cloud-enum` | Cloud asset (S3/GCP bucket) enumeration |
| `-f passive` | Passive only (does not touch the target) |
| `-f active` | Allow active probing |
| `-o .` | Output directory |
| `--output-modules neo4j` | Push the results straight into neo4j |

## Attack Scenario Playbook

### One-stop full asset mapping

```bash
bbot -t corp.com -p subdomain-enum web-basic cloud-enum -f passive -o out
# out/ contains JSON/CSV/TXT with all assets and URLs
```

### Passive first, then active gap filling

```bash
bbot -t corp.com -p subdomain-enum -f passive
bbot -t corp.com -p web-basic -f active -o out2
```

## Notes

Modular pipeline design where presets decide which modules run; passive mode sends no packets to the target, which is friendly to compliance requirements.
