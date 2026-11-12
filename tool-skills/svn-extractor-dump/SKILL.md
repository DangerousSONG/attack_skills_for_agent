---
name: svn-extractor-dump
description: "svn-extractor recovers source from leaked .svn directories. Signals: attack surface, cloud assets, SVN leak export, filtering"
zh-signals: "svn-extractor: .svn 泄露源码恢复。信号:攻击面,云资产,SVN 泄露导出,过滤。"
when-to-use: >-
  Use when a target exposes a .svn directory and you need to recover leaked
  source code from the SVN metadata, with optional file-type filtering.
---

# svn-extractor

- Attack Category: C05 External Attack Surface and Cloud Asset Exposure
- Upstream Repository: https://github.com/anantshri/svn-extractor
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/anantshri/svn-extractor && cd svn-extractor
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 svn_extractor.py --url https://t.com/.svn/entries` | SVN leak export |
| `--url url --output out/` | Output |
| `--match '.*.php'` | Filtering |

## Attack Scenario Playbook

### Recovering source code from a .svn leak

```bash
python3 svn_extractor.py --url https://t.com/.svn/entries --output src/
# Like GitTools but targeting SVN
```

## Notes

Tool for exploiting exposed SVN directories.
