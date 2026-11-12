---
name: dcrawl-fast-crawl
description: "dcrawl: Performs lightweight batch URL crawling. Signals: asset mapping, subdomains, fast batch crawling, depth."
zh-signals: "dcrawl: 批量 URL 轻爬。信号:资产测绘,子域名,批量快速爬取,深度。"
when-to-use: >-
  Use for fast, lightweight batch URL crawling that extracts only links without
  fetching content, suited to large asset lists.
---

# dcrawl

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/kgretzky/dcrawl
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/kgretzky/dcrawl@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `dcrawl -list urls.txt` | Fast batch crawling |
| `-depth 2` | Depth |
| `-out out.txt` | Output |
| `-timeout 5` | Timeout |

## Attack Scenario Playbook

### Lightweight batch URL crawling

```bash
dcrawl -list alive.txt -depth 2
# Extracts links only without fetching content, extremely fast
```

## Notes

By kgretzky, a pure link-extraction crawler that is faster than htcap.
