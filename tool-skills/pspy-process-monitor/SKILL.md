---
name: pspy-process-monitor
description: "pspy: Captures scheduled-task privilege escalation clues. Signals: internal enumeration, network discovery, monitor process forks only, print interval, highlight new processes."
zh-signals: "pspy: 定时任务提权线索捕捉。信号:内网枚举,网络发现,只监控进程 fork,打印间隔,高亮新进程。"
when-to-use: >-
  Use after gaining a non-root Linux foothold to monitor processes and cron jobs
  and uncover privilege-escalation paths.
---

# pspy

- Attack Category: C29 Internal Network Discovery and Enumeration
- Upstream Repository: https://github.com/DominicBreuker/pspy
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
Download the pspy64 / pspy32 static binaries from the release page
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./pspy64` | Monitor all processes and scheduled tasks (no root required) |
| `-pf` | Monitor process forks only |
| `-i 1000` | Print interval |
| `-c` | Highlight new processes |

## Attack Scenario Playbook

### Capturing Scheduled Task Privilege Escalation Clues

```bash
./pspy64  # Observe which scripts/binaries root cron calls, look for writable paths to hijack
```

## Notes

Four variants of 64/32-bit and static/dynamic builds; use pspy32s for containers and old kernels.
