---
name: waybackpack-archive
description: "waybackpack: Historical snapshot forensics. Signals: asset mapping, subdomains, list archived URLs, list only no download, from 2015."
zh-signals: "waybackpack: 历史快照取证。信号:资产测绘,子域名,列归档 URL,只列不下载,从 2015 年。"
when-to-use: >-
  Use when mapping historical versions of a target domain and you want to list
  or download Wayback Machine snapshots to find retired endpoints, comments, or
  hardcoded secrets.
---

# waybackpack

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/jsvine/waybackpack
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install waybackpack
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `waybackpack target.com` | List archived URLs |
| `--list` | List only, do not download |
| `-d 2015` | From 2015 onwards |
| `--uniques-only` | Deduplicate |
| `-o dir` | Download snapshots |

## Attack Scenario Playbook

### Historical Snapshot Forensics

```bash
waybackpack corp.com -d 2018 --uniques-only -o snapshots/
# Browse old pages for retired endpoints, keys in comments, and hardcoded addresses
```

## Notes

Pull whole Wayback snapshots locally to diff historical changes; purpose-built for finding 'secrets that were once exposed'.
