---
name: richsploit-richdesk
description: "Richsploit: Exploits rich client vulnerabilities. Signals: pwn, binary exploitation, list."
zh-signals: "Richsploit: 富客户端漏洞利用。信号:pwn,二进制利用,列表。"
when-to-use: >-
  Use when targeting rich-client or Windows desktop applications during a red-team engagement and
  you need a known CVE exploit module.
---

# Richsploit

- Attack Category: C46 Binary Exploitation and Pwn
- Upstream Repository: https://github.com/redtimmy/Richsploit
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/redtimmy/Richsploit && cd Richsploit
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 richsploit.py -f exploit -t 10.0.0.5` | RichClient exploitation |
| `-l` | List |
| `-c cmd` | Command |

## Attack Scenario Playbook

### Rich Client Exploitation

```bash
python3 richsploit.py -t target -f rce
# CVE-2020-0932 etc.
```

## Notes

A red-team rich client exploitation framework.
