---
name: gowitness-screenshot
description: "gowitness visualizes assets for triage and fingerprinting. Signals: asset mapping, subdomains, single URL screenshot and fingerprint, bulk screenshots, result browsing service."
zh-signals: "gowitness: 资产可视化核查(先看脸再决定打谁)。信号:资产测绘,子域名,单 URL 截图+指纹,批量截图,启动结果浏览服务。"
when-to-use: "Use during asset mapping to screenshot and fingerprint single or bulk URLs for visual triage and deciding what to attack. Requires httpx-style URL input and stores results in SQLite for browsing."
---

# gowitness

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/sensepost/gowitness
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/sensepost/gowitness@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `gowitness scan --url https://target.com` | Single URL screenshot plus fingerprint |
| `file -f urls.txt --threads 20` | Bulk screenshots |
| `server` | Start the result browsing service |
| `report export -f csv` | Export report |

## Attack Scenario Playbook

### Visual asset triage (look before you decide who to attack)

```bash
naabu -host target.com -top-ports 1000 | httpx | gowitness file -f - --threads 30
gowitness server  # Browse the screenshots to pick admin panels
```

## Notes

Headless Chrome screenshots stored in SQLite, works best paired with an httpx pipeline.
