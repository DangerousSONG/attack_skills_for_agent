---
name: fuzzdb-payload-dict
description: "fuzzdb supports manual fuzzing payload construction. Signals: web scanning, vulnerability scanning, path dictionaries, error fingerprint regex, weak password dictionaries."
zh-signals: "fuzzdb: 手工构造模糊测试。信号:web扫描,漏洞扫描,路径字典,错误指纹正则,弱口令字典。"
when-to-use: >-
  Use when building manual fuzzing payloads for web scanning and you need ready-made
  path dictionaries, attack payloads, error fingerprint regexes, or weak password lists.
---

# fuzzdb

- Attack Category: C41 Web Vulnerability Scanning and Validation
- Upstream Repository: https://github.com/fuzzdb-project/fuzzdb
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/fuzzdb-project/fuzzdb
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `discovery-predictable-filepaths/` | Path dictionaries |
| `attack-payloads/` | Payload sets per vulnerability type |
| `regex/` | Error fingerprint regexes |
| `wordlists-user-passwd/` | Weak password dictionaries |

## Attack Scenario Playbook

### Manual fuzzing payload construction

```bash
ffuf -u https://t.com/FUZZ -w fuzzdb/discovery-payloads/.../common.txt
sqlmap -r req.txt --prefix-file=fuzzdb/attack-payloads/sql-injection/detect/...
```

## Notes

A classic fuzzing corpus that complements SecLists; there is no code, only wordlists, so agents can reference the paths directly.