---
name: ropeadope-logclean
description: "ropeadope: Cleans Linux host logs. Signals: trace cleanup, anti-forensics, clear login records, clear authentication logs."
zh-signals: "ropeadope: Linux 主机日志清理。信号:痕迹清理,反取证,清登录记录,清认证日志。"
when-to-use: >-
  Use when cleaning Linux host logs after an authorized red-team action and you need to clear
  wtmp, btmp, auth logs, lastlog, and shell history.
---

# ropeadope

- Attack Category: C20 Anti-Forensics and Trace Cleanup
- Upstream Repository: https://github.com/BullsEye0/ropeadope
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/BullsEye0/ropeadope && chmod +x ropeadope.sh
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./ropeadope.sh` | Interactive Linux log cleanup |
| `--wtmp` | Clear login records |
| `--auth` | Clear authentication logs |
| `--shell` | Clear shell history |

## Attack Scenario Playbook

### Linux host log cleanup

```bash
./ropeadope.sh  # Use the menu to clear wtmp/btmp/auth.log/lastlog/shell history
```

## Notes

Script-based tool requiring root; clearing logs is a highly sensitive operation, so snapshot the evidence first in authorized exercises.
