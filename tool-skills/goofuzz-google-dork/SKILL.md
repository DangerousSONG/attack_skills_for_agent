---
name: goofuzz-google-dork
description: "GooFuzz performs Google dorking without an API key. Signals: web vulnerabilities, injection, /backup, file types."
zh-signals: "GooFuzz: 免 API key 的 Google dork。信号:web漏洞,注入,/backup'`,文件类型。"
when-to-use: >-
  Use when doing Google dorking without an API key to discover exposed sensitive
  files, directories and indexed content on a target domain.
---

# GooFuzz

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/m3n0sd0n4ld/GooFuzz
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/m3n0sd0n4ld/GooFuzz && cd GooFuzz
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./GooFuzz -t corp.com` | Google dork bulk probing |
| `-t target -d '/admin|/backup'` | Custom dork |
| `-e pdf,xls` | File types |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Google Dork Without an API Key

```bash
./GooFuzz -t corp.com -w wordlists/ghdb.txt
# Auto-paginates to harvest results, hunting for indexed sensitive files on the target
```

## Notes

A pure bash Google dorking tool that needs no API key and ships with the categorized GHDB wordlists.
