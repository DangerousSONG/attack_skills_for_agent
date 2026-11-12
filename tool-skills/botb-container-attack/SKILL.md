---
name: botb-container-attack
description: "botb (Break Out The Box): assesses and escapes containers. Signals: cloud command execution, container escape, static container analysis, specify socket, enumeration only"
zh-signals: "botb (Break Out The Box): 容器评估+逃逸一体。信号:云命令执行,容器逃逸,静态容器分析,指定 socket,仅枚举。"
when-to-use: "Use botb when you have a foothold inside a container and need to statically analyze it and attempt escape, including Docker socket and dockerd discovery, during cloud or container engagements."
---

# botb (Break Out The Box)

- Attack Category: C14 Cloud and Container Execution
- Upstream Repository: https://github.com/brompwnie/botb
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/brompwnie/botb@latest or take the release binary
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `botb -analyze` | Static container analysis |
| `-socketpath /var/run/docker.sock` | Specify socket |
| `-recon` | Enumeration only |
| `-exploit` | Perform escape |
| `-findDockerd` | Locate dockerd |

## Attack Scenario Playbook

### Container Assessment and Escape in One Tool

```bash
botb -analyze  # Output: capabilities/mounts/env secrets/escape feasibility score
botb -analyze -exploit
```

## Notes

A single Go file that is easy to drop into a container; complements deepce (botb focuses on static analysis).
