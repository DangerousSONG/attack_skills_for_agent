---
name: uptux-linux-check
description: "uptux: Linux systemd privilege escalation detection. Signals: linux privilege escalation, SUID, Linux privilege escalation check, full check, verbose."
zh-signals: "uptux: Linux systemd 提权检测。信号:linux提权,suid,Linux 提权检查,全检查,详细。"
when-to-use: >-
  Use after gaining a low-privilege Linux shell to enumerate systemd units, timers, sockets and SUID misconfigurations that may enable local privilege escalation.
---

# uptux

- Attack Category: C16 Linux Local Privilege Escalation
- Upstream Repository: https://github.com/initstring/uptux
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/initstring/uptux
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 uptux.py` | Linux privilege escalation check |
| `-a` | Full check |
| `-d` | Verbose |

## Attack Scenario Playbook

### Linux systemd privilege escalation detection

```bash
python3 uptux.py
# Privilege escalation via systemd units, timers and sockets
```

## Notes

Linux privilege escalation enumeration focused on systemd.
