---
name: amass-attack-surface
description: "Amass: performs full subdomain enumeration and attack surface mapping, enhanced with API keys. Signals: asset mapping, subdomain, passive+active enumeration, passive-only"
zh-signals: "Amass: 子域名全量枚举与攻击面测绘、带 API key 的增强枚举。信号:资产测绘,子域名,被动+主动枚举,纯被动。"
when-to-use: >-
  Use when enumerating a target domain's subdomains and attack surface, either
  passive-only for stealth or passive+active, optionally with API keys for richer sources.
---

# Amass

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/owasp-amass/amass
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/owasp-amass/amass/v4/...@master or snap install amass
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `amass enum -d target.com` | Passive + active enumeration |
| `-passive` | Passive only |
| `-active` | Active probing including TLS fingerprinting |
| `-src -v` | Show the data sources |
| `-o out.txt` | Output |
| `amass intel -d target.com -whois` | ASN/whois intelligence |
| `-config config.ini` | API key configuration |

## Attack Scenario Playbook

### Full subdomain enumeration and attack surface mapping

```bash
amass enum -d corp.com -active -o subs.txt
amass intel -d corp.com -whois  # find related ASNs/domains
```

### Enhanced enumeration with API keys

```bash
amass enum -d target.com -config ~/.config/amass/config.ini -passive
```

## Notes

An OWASP project and the most complete mapping tool in terms of data sources; configuring Shodan/Censys and other API keys in config.ini improves the results significantly.
