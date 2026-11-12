---
name: waymore-archive-urls
description: "waymore: Historical URL full harvesting. Signals: asset mapping, subdomains, URL only, upper limit."
zh-signals: "waymore: 历史 URL 全量收割。信号:资产测绘,子域名,仅 URL,上限。"
when-to-use: >-
  Use when harvesting historical URLs of a target domain from Wayback Machine,
  Common Crawl and AlienVault OTX for asset discovery. The consolidated URL
  list feeds downstream parameter fuzzing or content discovery.
---

# waymore

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/xnl-h4ck3r/waymore
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install waymore
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `waymore -i t.com` | Wayback+CC+OTX URL harvesting |
| `-i t.com -mode U` | URLs only |
| `-i t.com -oU out.txt` | Output |
| `-n 50000` | Upper limit |

## Attack Scenario Playbook

### Full historical URL harvesting

```bash
waymore -i corp.com -oU urls.txt
# More complete than waybackurls (includes CC/OTX), feeds dalfox
```

## Notes

By xnl-h4ck3r, extracts URLs from three sources (Wayback/Common Crawl/AlienVault), well suited to large-scale asset discovery.
