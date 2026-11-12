---
name: name-that-hash
description: "name-that-hash: Identify unknown hash types. Signals: password cracking, hash cracking, identify hash, batch files, silent."
zh-signals: "name-that-hash: 未知哈希类型识别。信号:密码破解,哈希破解,识别哈希,批量文件,静默。"
when-to-use: >-
  Use when you have unknown or dumped password hashes and need to identify their algorithm
  before selecting the correct hashcat or John mode.
---

# name-that-hash

- Attack Category: C25 Hash and Password Cracking
- Upstream Repository: https://github.com/HashPals/Name-That-Hash
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install name-that-hash
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `nth -t '5f4dcc3b5aa765d61d8327deb882cf99'` | Identify hash |
| `-f hashes.txt` | Batch file |
| `--no-banner` | Quiet |
| `-j` | JSON output |

## Attack Scenario Playbook

### Unknown hash type identification

```bash
nth -f dumped_hashes.txt -j | jq '.[].hashcat'
# Output 300+ algorithm matches with the corresponding hashcat -m numbers, ready for cracking
```

## Notes

Identifies 300+ hash formats and provides hashcat/John arguments; complements hashid, run both.
