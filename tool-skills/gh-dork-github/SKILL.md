---
name: gh-dork-github
description: "gh-dork dorks organization sensitive files. Signals: attack surface, cloud assets, organization repository dork, custom queries, threads."
zh-signals: "gh-dork: 组织敏感文件 dork。信号:攻击面,云资产,组织仓库 dork,自定义,线程。"
when-to-use: >-
  Use when searching GitHub organization repositories for sensitive files such
  as passwords, env files, and keys. Supports custom dork lists and thread
  control.
---

# gh-dork

- Attack Category: C05 External Attack Surface and Cloud Asset Exposure
- Upstream Repository: https://github.com/micha3lb3/gh-dork
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/micha3lb3/gh-dork && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 gh-dork.py -u targetcorp` | Organization repository dork |
| `-u org -d dorks.txt` | Custom |
| `-t 20` | Threads |

## Attack Scenario Playbook

### Organization Sensitive File Dorking

```bash
python3 gh-dork.py -u corp
# Search password/env/key file names
```

## Notes

Sensitive file search across GitHub organization repositories.
