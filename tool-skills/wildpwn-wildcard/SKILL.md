---
name: wildpwn-wildcard
description: "wildpwn: tar/chmod wildcard privilege escalation. Signals: linux privilege escalation, SUID, wildcard injection."
zh-signals: "wildpwn: tar/chmod 通配符提权。信号:linux提权,suid,通配符注入。"
when-to-use: >-
  Use during Linux privilege escalation when root-run tar or chmod commands
  process wildcard characters in a writable directory.
---

# wildpwn

- Attack Category: C16 Linux Local Privilege Escalation
- Upstream Repository: https://github.com/localh0t/wildpwn
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/localh0t/wildpwn
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python wildpwn.py combined /var/www` | Wildcard injection |
| `--file file` | Specify |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### tar/chmod Wildcard Privilege Escalation

```bash
python wildpwn.py tar /backup
# Escalate via checkpoint
```

## Notes

A wildcard injection privilege escalation tool.
