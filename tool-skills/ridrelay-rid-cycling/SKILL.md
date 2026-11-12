---
name: ridrelay-rid-cycling
description: "ridrelay: Enumerates users via anonymous/empty sessions. Signals: internal enumeration, network discovery, RID cycling for domain users, specified RID range, attempt SAM enumeration."
zh-signals: "ridrelay: 匿名/空会话用户枚举。信号:内网枚举,网络发现,RID 循环枚举域用户,指定 RID 范围,尝试 SAM 枚举。"
when-to-use: >-
  Use during internal AD enumeration when you have little or no credentials and
  want to enumerate domain users via SMB null sessions and RID cycling.
---

# ridrelay

- Attack Category: C29 AD and LDAP Enumeration
- Upstream Repository: https://github.com/skorov/ridrelay
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/skorov/ridrelay && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python ridrelay.py -t 10.0.0.5` | RID cycling to enumerate domain users |
| `-t 10.0.0.5 -r 1000-2000` | Specify the RID range |
| `--sam` | Attempt SAM enumeration |
| `-o users.txt` | Output |

## Attack Scenario Playbook

### Anonymous/empty session user enumeration

```bash
python ridrelay.py -t 10.0.0.5
# Use null sessions to grab the domain user list, then pair with asreproast
```

## Notes

Uses SMB null sessions for RID cycling to enumerate domain users without credentials (automates an old trick).
