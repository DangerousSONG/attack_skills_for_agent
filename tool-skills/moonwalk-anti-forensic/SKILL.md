---
name: moonwalk-anti-forensic
description: "moonwalk: Linux trace timeline erasure. Signals: trace cleanup, anti-forensics, start timestamp baseline recording, active period, in-memory execution mode."
zh-signals: "moonwalk: Linux 痕迹时间线抹除。信号:痕迹清理,反取证,开始记录时间戳基线,活动期,内存执行模式。"
when-to-use: >-
  Use when you need to erase Linux forensic timeline evidence after operations by
  recording a timestamp baseline with `moonwalk start` and restoring all
  mtime/atime with `moonwalk finish`; supports in-memory mode and directory
  scoping.
---

# moonwalk

- Attack Category: C20 Anti-Forensics and Trace Cleanup
- Upstream Repository: https://github.com/mufeedvh/moonwalk
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
cargo install moonwalk or take the release binary
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `moonwalk start` | Start recording the timestamp baseline |
| `perform operations...` | Active period |
| `moonwalk finish` | Restore all mtime/atime |
| `-m` | In-memory execution mode |
| `-d dir` | Limit to a directory |

## Attack Scenario Playbook

### Erase the Linux trace timeline

```bash
moonwalk start
# Perform the intrusion operations (file access/modification)
moonwalk finish  # all timestamps are restored to the baseline, breaking the audit timeline
```

## Notes

Anti-forensics written in Rust that restores the file timeline; pair it with mat2 to clear metadata and form a complete cleanup chain.
