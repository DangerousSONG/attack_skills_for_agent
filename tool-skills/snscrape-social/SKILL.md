---
name: snscrape-social
description: "snscrape: reconstructs target social footprint and timeline. Signals: email collection, employee info, fetch user tweets, search syntax, single tweet."
zh-signals: "snscrape: 目标社交足迹与时间线重建。信号:邮箱收集,员工信息,拉取用户推文,搜索语法,单条推文。"
when-to-use: "Use when reconstructing a target's social footprint and timeline from public posts for OSINT, including emails and employee details. Requires a target username or search query and Python."
---

# snscrape

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/JustAnotherArchivist/snscrape
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install snscrape
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `snscrape --jsonl twitter-user target > t.jsonl` | Fetch user tweets |
| `twitter-search 'from:user since:2023-01-01'` | Search syntax |
| `twitter-tweet url` | Single tweet |
| `instagram-user user` | IG public profile (restricted) |

## Attack Scenario Playbook

### Reconstruct the target's social footprint and timeline

```bash
snscrape --jsonl twitter-user victim | jq -r '.content' | head -100
# Locate workplace/colleague relationships/password hint style information
```

## Notes

Purely passive scraping of public pages; the Twitter interface changes frequently, so when it breaks, retry with a smaller --max-results.
