---
name: mrkaplan-event-clean
description: "MrKaplan: Post-action targeted event log cleanup. Signals: red team, methodology, erase mode keep 1102, target event/log configuration, self-delete after run."
zh-signals: "MrKaplan: 行动后事件日志定点清理。信号:红队,方法论,擦除模式(留 1102),目标事件/日志配置,运行后自删。"
when-to-use: >-
  Use when cleaning up Windows event logs after an authorized red-team action and you need
  targeted removal of specific event IDs while keeping log 1102 intact.
---

# MrKaplan

- Attack Category: C50 Trace Cleanup and Anti-Forensics
- Upstream Repository: https://github.com/Idov31/MrKaplan
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/Idov31/MrKaplan && build MrKaplan
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `MrKaplan.exe --operation disguise` | Disguise mode (deletes without leaving a 1102 trace) |
| `--operation erase` | Erase mode (keeps 1102) |
| `config.yaml` | Target event/log configuration |
| `-d` | Self-delete after running |

## Attack Scenario Playbook

### Targeted Event Log Cleanup After an Action

```bash
MrKaplan.exe --operation disguise -c config.yaml
# Only deletes the events listed in config, clearing key traces such as 4624/4672
```

## Notes

Targeted Windows event log cleanup, more covert than wiping everything with wevtutil cl (which raises an alert), and disguise mode does not trigger 1102.
