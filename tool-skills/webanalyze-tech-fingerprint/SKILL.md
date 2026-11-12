---
name: webanalyze-tech-fingerprint
description: "webanalyze: Technology stack fingerprinting for CVE selection. Signals: asset mapping, subdomains, batch technology stack identification, single target, crawl page count."
zh-signals: "webanalyze: 技术栈指纹识别(挑 CVE 用)。信号:资产测绘,子域名,批量技术栈识别,单目标,爬取页数。"
when-to-use: >-
  Use during asset mapping to fingerprint technology stacks in batch and map
  identified components to known CVEs.
---

# webanalyze

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/rverton/webanalyze
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/rverton/webanalyze@latest && webanalyze -update
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `webanalyze -hosts hosts.txt` | Batch technology stack identification |
| `-host https://x.com` | Single target |
| `-crawl 3` | Crawl page count |
| `-apps apps.json` | Custom fingerprint database |
| `-output csv` | CSV output |

## Attack Scenario Playbook

### Technology Stack Fingerprinting (for Picking CVEs)

```bash
httpx -l subs.txt -silent | webanalyze -hosts - -output csv
# Filter by fingerprint: grep -i 'wordpress\|jenkins\|shiro' tech.csv
```

## Notes

A Go port of Wappalyzer, suitable for large-scale batch fingerprinting; identified components map directly to vulnerability databases.
