---
name: subjs-js-extract
description: "subjs batch-extracts JavaScript files. Signals: web vulnerability, injection, subjs, concurrency"
zh-signals: "subjs: JS 文件批量提取。信号:web漏洞,注入,subjs`,并发。"
when-to-use: >-
  Use to batch-extract JavaScript file URLs from a list of web pages, feeding
  the results into secret or vulnerability scanners.
---

# subjs

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/lc/subjs
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/lc/subjs@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `cat urls.txt | subjs` | Extract JS links from URLs |
| `-c 20` | Concurrency |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Batch JavaScript File Extraction

```bash
cat gau_urls.txt | subjs | tee js.txt
# feed the results into nuclei/secret scanning
```

## Notes

Batch-extracts <script src> from HTML pages; often used together with gau.
