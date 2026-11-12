---
name: onionsearch-darkweb
description: "Multi-engine dark web intelligence aggregation. Signals: web vulnerability, injection, multi dark-web engine search, pages, specified engines."
zh-signals: "OnionSearch: 多引擎暗网情报聚合。信号:web漏洞,注入,多暗网引擎搜索,页数,指定引擎。"
when-to-use: >-
  Use when gathering threat intelligence about an authorized target from multiple dark-web
  search engines and you need aggregated results across engines.
---

# OnionSearch

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/megadose/OnionSearch
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install onionsearch
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `onionsearch 'target'` | Multi dark-web engine search |
| `-p 5` | Pages |
| `--engines ahmia,tor66` | Specified engines |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Multi-Engine Dark Web Intelligence Aggregation

```bash
onionsearch 'corp.com'
# Query 8+ dark web engines such as ahmia/tor66 in one shot
```

## Notes

By megadose, aggregates multiple dark web search engines for threat intelligence collection on a target.
