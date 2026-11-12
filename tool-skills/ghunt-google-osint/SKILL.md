---
name: ghunt-google-osint
description: "GHunt reverse-searches Google footprints from email. Signals: email collection, employee information, GAIA ID lookup, map review account correlation."
zh-signals: "GHunt: 邮箱反查 Google 足迹。信号:邮箱收集,员工信息,GAIA ID 反查,地图评价账号关联。"
when-to-use: >-
  Use when you have a Gmail address and want to reverse-search public Google
  footprints such as profile, map reviews and YouTube channels (needs logged-in cookies).
---

# GHunt

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/mxrch/GHunt
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/mxrch/GHunt && cd GHunt && pip install -r requirements.txt && python ghunt.py login
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `ghunt email victim@gmail.com` | Email → Google account profile |
| `ghunt gaia <id>` | GAIA ID reverse lookup |
| `ghunt review <place_id>` | Map review account correlation |

## Attack Scenario Playbook

### Reverse-Search Google Footprints from an Email

```bash
python ghunt.py email target@gmail.com
# Returns public traces such as G+ avatar, map reviews and YouTube channels
```

## Notes

Requires running login first to inject cookies (exported by the GHunt browser extension); it only queries public data.
