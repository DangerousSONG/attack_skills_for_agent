---
name: websploit-wifi-dos
description: "websploit: Web vulnerability rapid exploitation. Signals: pwn, binary exploitation, web attack framework, modules."
zh-signals: "websploit: Web 漏洞快速利用。信号:pwn,二进制利用,Web 攻击框架,模块。"
when-to-use: "Use when running web attack modules from a framework to quickly exploit common web vulnerabilities on a target."
---

# websploit

- Attack Category: C46 Binary Exploitation and Pwn
- Upstream Repository: https://github.com/f4rih/websploit
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install websploit
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `websploit` | Web attack framework |
| `use web/dir_scanner` | Module |
| `set TARGET t.com` | Target |
| `run` | Execute |

## Attack Scenario Playbook

### Rapid web vulnerability exploitation

```bash
websploit && use web/wordpress_scanner
# One module, one vulnerability
```

## Notes

A web penetration framework where each module maps to a CVE.
