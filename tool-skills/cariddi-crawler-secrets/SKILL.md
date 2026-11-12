---
name: cariddi-crawler-secrets
description: "cariddi: Harvests secrets from source code. Signals: API attack, interface testing, cariddi, crawl only without scanning, extension filtering."
zh-signals: "cariddi: 源码级秘密收割。信号:api攻击,接口测试,cariddi`,只爬不扫描,扩展名过滤。"
when-to-use: >-
  Use to crawl targets and harvest secrets such as API keys, tokens, and
  internal endpoints from source code and responses.
---

# cariddi

- Attack Category: C10 API and Business Logic Attacks
- Upstream Repository: https://github.com/edoardottt/cariddi
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/edoardottt/cariddi@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `cat hosts.txt | cariddi` | Crawl the site and extract secrets |
| `-s` | Crawl only, no scanning |
| `-e php,jsp` | Extension filtering |
| `-d 3` | Crawl depth |
| `-i ignore.txt` | Ignore paths |
| `-headers` | Output headers |
| `-secrets` | Enable secret scanning |

## Attack Scenario Playbook

### Source-Code-Level Secret Harvesting

```bash
echo https://target.com | cariddi -s -d 3 | tee urls.txt
cat urls.txt | cariddi -secrets -headers  # Extract API keys/tokens/internal addresses
```

## Notes

A fast crawler written in Go whose secret-extraction regexes cover 40+ patterns; pipeline friendly.
