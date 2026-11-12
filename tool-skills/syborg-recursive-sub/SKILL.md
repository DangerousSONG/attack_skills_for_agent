---
name: syborg-recursive-sub
description: "Syborg brute-forces recursively while avoiding wildcards. Signals: asset mapping, subdomain, recursive subdomain enumeration, resolver"
zh-signals: "Syborg: 递归+通配符规避爆破。信号:资产测绘,子域名,递归子域枚举,resolver。"
when-to-use: >-
  Use during subdomain enumeration when you need recursive brute-forcing that
  avoids wildcard false positives, with custom resolvers.
---

# Syborg

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/MustafaTanguner/Syborg
- Upstream License: NOASSERTION (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/MustafaTanguner/Syborg
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python syborg.py corp.com -w wordlist.txt` | Recursive subdomain enumeration |
| `-r resolvers.txt` | resolver |

## Attack Scenario Playbook

### Recursive Brute-Force with Wildcard Evasion

```bash
python syborg.py corp.com -w all.txt  # recursive brute-force of deep subdomains such as dev.x.corp.com
```

## Notes

Recursive enumeration mode plus Sublist3r-style multi-source aggregation.
