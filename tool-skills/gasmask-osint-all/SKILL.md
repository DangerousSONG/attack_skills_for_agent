---
name: gasmask-osint-all
description: "GasMask performs multi-mode OSINT for domains, names, and companies. Signals: asset mapping, subdomains, full OSINT, subdomain, GitHub."
zh-signals: "GasMask: 域名/人名/公司多模式 OSINT。信号:资产测绘,子域名,全量 OSINT,子域,github。"
when-to-use: >-
  Use when running multi-mode OSINT for a domain, person name or company,
  covering full OSINT, subdomains and GitHub.
---

# GasMask

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/twelvesec/gasmask
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/twelvesec/gasmask && cd gasmask && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python gasmask.py -d target.com -A` | Full OSINT |
| `-s` | Subdomains |
| `-g` | github |
| `-t` | twitter |
| `-b` | shodan |

## Attack Scenario Playbook

### Multi-Mode OSINT for Domains, Names and Companies

```bash
python gasmask.py -d corp.com -A  # Aggregate DNS/subdomains/email/whois/GitHub/Shodan
```

## Notes

A multi-mode OSINT aggregator by twelvesec; supports lookup by company name or person name.
