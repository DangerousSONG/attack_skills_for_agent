---
name: waybackurls-history
description: "waybackurls: Historical URL harvesting. Signals: asset mapping, subdomains, with timestamps, without subdomains, waybackurls."
zh-signals: "waybackurls: 历史 URL 收割。信号:资产测绘,子域名,带时间戳,不含子域,waybackurls`。"
when-to-use: "Use during asset mapping to harvest historical URLs from the Wayback Machine and surface sensitive endpoints."
---

# waybackurls

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/tomnomnom/waybackurls
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/tomnomnom/waybackurls@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `waybackurls corp.com` | Pull all Wayback URLs |
| `-dates` | Include timestamps |
| `-no-subs` | Exclude subdomains |
| `cat domains.txt | waybackurls` | Batch |

## Attack Scenario Playbook

### Historical URL Harvesting

```bash
echo corp.com | waybackurls | sort -u > urls.txt
grep -Ei 'login|admin|token|key' urls.txt  # Test sensitive endpoints first
```

## Notes

Passive data source pipeline by tomnomnom; complements gau, and running both reduces omissions.
