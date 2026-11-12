---
name: gitmails-osint
description: "gitmails harvests developer emails. Signals: attack surface, cloud assets, repository committer email extraction, depth."
zh-signals: "gitmails: 开发者邮箱收割。信号:攻击面,云资产,仓库提交者邮箱提取,深度。"
when-to-use: >-
  Use when harvesting developer email addresses and usernames from the commit history of
  authorized public repositories to enrich OSINT and attack surface mapping.
---

# gitmails

- Attack Category: C05 External Attack Surface and Cloud Asset Exposure
- Upstream Repository: https://github.com/mazen160/gitmails
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install gitmails
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `gitmails -u github.com/target` | Repository committer email extraction |
| `-u url -d 3` | Depth |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Developer Email Harvesting

```bash
gitmails -u github.com/corp/internal-tool
# employee emails + usernames
```

## Notes

Extracts emails from git repository commit history.
