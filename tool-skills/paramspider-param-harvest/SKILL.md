---
name: paramspider-param-harvest
description: "Harvest parameterized URLs for vulnerability scanners. Signals: data collection, packaging, high crawl depth, exclude extensions."
zh-signals: "ParamSpider: 带参 URL 批量收割(喂漏洞扫描器)。信号:数据收集,打包,高爬取深度,排除扩展。"
when-to-use: >-
  Use when preparing for automated vulnerability scanning and you need to
  harvest parameterized URLs for a target domain from web archives; supports
  crawl depth and extension exclusion, feeding tools like dalfox or sqlmap.
---

# ParamSpider

- Attack Category: C33 URL and Content Discovery
- Upstream Repository: https://github.com/devanshbatham/ParamSpider
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/devanshbatham/ParamSpider && cd ParamSpider && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 paramspider.py -d target.com` | Extract parameterized URLs from web archives |
| `-d target.com -l high` | High crawl depth |
| `-e php,aspx` | Exclude extensions |
| `-o params.txt` | Output |

## Attack Scenario Playbook

### Batch harvesting parameterized URLs (feeding vulnerability scanners)

```bash
python3 paramspider.py -d corp.com -l high -o urls.txt
# Hand off to dalfox/sqlmap to batch test XSS/SQLi
```

## Notes

Extracts parameterized URLs for the target domain from Wayback and other crawl sources, saving you from manually digging through archives, a must-have prerequisite for automated scanning.
