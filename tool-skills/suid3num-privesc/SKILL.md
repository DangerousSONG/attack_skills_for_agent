---
name: suid3num-privesc
description: "suid3num finds SUID privilege escalation paths. Signals: Linux privilege escalation, suid, SUID enumeration, exploit, list"
zh-signals: "suid3num: SUID 提权路径。信号:linux提权,suid,SUID 枚举,exploit,列表。"
when-to-use: >-
  Use when you have a shell on an authorized Linux host and need to enumerate SUID binaries
  and identify GTFOBins-style privilege escalation paths.
---

# suid3num

- Attack Category: C16 Linux Local Privilege Escalation
- Upstream Repository: https://github.com/Anon-Exploiter/SUID3NUM
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/Anon-Exploiter/SUID3NUM
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 suid3num.py` | SUID enumeration |
| `-e` | exploit |
| `-l` | List |

## Attack Scenario Playbook

### SUID Privilege Escalation Paths

```bash
python3 suid3num.py
# one-shot privilege escalation with GTFOBins
```

## Notes

Automatic SUID binary enumeration and exploitation.
