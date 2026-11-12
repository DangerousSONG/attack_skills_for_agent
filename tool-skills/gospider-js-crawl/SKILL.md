---
name: gospider-js-crawl
description: "gospider extracts JavaScript endpoints for vulnerability scanning. Signals: web vulnerabilities, injection, bulk scanning, depth, JS endpoint extraction."
zh-signals: "gospider: JS 端点提取喂漏扫。信号:web漏洞,注入,批量,深度,解析 JS 提取端点。"
when-to-use: >-
  Use when crawling web targets to collect URLs, forms and JavaScript-derived API endpoints as input for vulnerability scanners like nuclei or dalfox.
---

# gospider

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/jaeles-project/gospider
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/jaeles-project/gospider@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `gospider -s https://t.com` | Full-site crawl (URL/JS/forms) |
| `-S urls.txt` | Batch |
| `-d 3` | Depth |
| `--js` | Parse JS to extract endpoints |
| `-o out/` | Output |
| `-t 20` | Threads |

## Attack Scenario Playbook

### JS endpoint extraction feeds the vulnerability scanner

```bash
gospider -S live_hosts.txt -d 3 --js -o spider/
# Extract API endpoints/parameters from JS bundles, hand off to dalfox/nuclei
```

## Notes

Crawler from the jaeles ecosystem, JS rendering plus source map parsing, outputs a URL list that plugs straight into nuclei/dalfox.
