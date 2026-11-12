---
name: sandcastle-s3
description: "sandcastle: Brute-forces S3 bucket names. Signals: attack surface, cloud assets, S3 bucket discovery, dictionary."
zh-signals: "sandcastle: S3 桶名爆破。信号:攻击面,云资产,S3 bucket 发现,字典。"
when-to-use: >-
  Use when hunting cloud assets and you need to brute-force S3 bucket names from
  a target keyword and naming patterns; supports custom dictionaries and output
  files.
---

# sandcastle

- Attack Category: C05 External Attack Surface and Cloud Asset Exposure
- Upstream Repository: https://github.com/0xSearches/sandcastle
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/0xSearches/sandcastle
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 sandcastle.py -t corp` | S3 bucket discovery |
| `-t target -b buckets.txt` | Wordlist |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### S3 Bucket Name Brute Force

```bash
python3 sandcastle.py -t corp
# Iterate over common naming patterns
```

## Notes

Lightweight S3 bucket enumeration.
