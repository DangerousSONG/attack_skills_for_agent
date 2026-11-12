---
name: wfuzz-web-fuzzer
description: "wfuzz: Full-position fuzzing. Signals: web scanning, vulnerability scanning, directory brute force, POST fuzz, header fuzz."
zh-signals: "wfuzz: 全位置模糊测试。信号:web扫描,漏洞扫描,目录爆破,POST fuzz,Header fuzz。"
when-to-use: >-
  Use when fuzzing any position of an HTTP request such as path, POST body or
  headers for directory discovery, parameter fuzzing or vulnerability
  scanning.
---

# wfuzz

- Attack Category: C41 Web Vulnerability Scanning and Validation
- Upstream Repository: https://github.com/xmendez/wfuzz
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install wfuzz
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `-w /usr/share/wfuzz/wordlist/general/common.txt https://t.com/FUZZ` | Directory brute force |
| `-w words.txt -d 'id=FUZZ&name=x'` | POST fuzz |
| `-w payloads.txt -H 'X-Header: FUZZ'` | Header fuzz |
| `--hc=404` | Hide 404 |
| `--hh=889` | Filter by length |
| `-t 50` | Threads |
| `-o csv` | Output |
| `-z list,admin-root-test` | Value list |

## Attack Scenario Playbook

### Full-Position Fuzzing

```bash
wfuzz -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words.txt --hc 404 https://target/FUZZ
wfuzz -w sql-errors.txt -d 'id=FUZZ' --hh=1200 https://target/search.php  # SQLi error fingerprint probing
```

## Notes

A long-standing benchmark for HTTP fuzzing; the FUZZ placeholder works in any position of the URL/POST/Header/Cookie.
