---
name: gau-url-history
description: "gau collects historical endpoints for vulnerability scanning and JS secret mining. Signals: asset mapping, subdomains, include subdomains, concurrency."
zh-signals: "gau (Get All URLs): 历史端点收集→喂给漏洞扫描、JS 文件敏感信息挖掘。信号:资产测绘,子域名,包含子域名,并发数。"
when-to-use: >-
  Use when you need historical endpoint URLs for a target domain, including
  subdomains, to feed vulnerability scanning or JS secret mining. It pulls
  passively from multiple archive sources without touching the target.
---

# gau (Get All URLs)

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/lc/gau
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/lc/gau/v2/cmd/gau@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `gau example.com` | Full-source pull from OTX+Wayback+CommonCrawl+URLScan |
| `--subs` | Include subdomains |
| `--threads 5` | Concurrency |
| `--blacklist png,jpg` | Filter out static resources |
| `--fc 404` | Filter by status code (requires saving with --json first) |

## Attack Scenario Playbook

### Historical Endpoint Collection → Feed to Vulnerability Scanning

```bash
gau --subs target.com | grep -E '\.(php|asp|aspx|jsp)' | sort -u > endpoints.txt
nuclei -l endpoints.txt -t exposures/
```

### Sensitive Information Mining in JS Files

```bash
gau target.com | grep '\.js$' | httpx -silent | tee js.txt
while read u; do curl -s $u | grep -Eo '(api[_-]?key|token|secret)[^,]{0,80}'; done < js.txt
```

## Notes

Passive historical data source that never touches the target, ideal for narrowing the intelligence surface within authorized boundaries.
