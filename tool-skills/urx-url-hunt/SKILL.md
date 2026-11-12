---
name: urx-url-hunt
description: "urx: Multi-source URL aggregation. Signals: data collection, packing, pipeline filtering, concurrency."
zh-signals: "urx: 多源 URL 聚合。信号:数据收集,打包,管道过滤,并发。"
when-to-use: >-
  Use during URL and content discovery to aggregate URLs from multiple passive
  sources such as Wayback, Common Crawl, and OTX, filter them through pipes, and
  feed downstream tools.
---

# urx

- Attack Category: C33 URL and Content Discovery
- Upstream Repository: https://github.com/hahwul/urx
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
cargo install urx
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `urx -u https://t.com` | Multi-source URL harvesting (Wayback/CC/OTX) |
| `--pipe 'grep admin'` | Pipeline filtering |
| `-o out.txt` | Output |
| `-c 50` | Concurrency |
| `--include-wayback --include-otx` | Specify data sources |

## Attack Scenario Playbook

### Multi-Source URL Aggregation

```bash
urx -u https://t.com --pipe 'grep -Ei "api|admin|token"' | tee gold.txt
# Results from each source are deduplicated while both the raw and deduplicated URLs are output
```

## Notes

High-speed URL aggregator written in Rust, querying multiple sources such as Wayback Machine/Common Crawl/AlienVault OTX in one go.
