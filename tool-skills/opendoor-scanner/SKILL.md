---
name: opendoor-scanner
description: "Directory scanning with multiple reports. Signals: web vulnerability, injection, wordlist, threads, specified paths."
zh-signals: "OpenDoor: 目录扫描+多报告。信号:web漏洞,注入,字典,线程,指定路径。"
when-to-use: >-
  Use when you need a multithreaded directory and admin panel scan of a web target with wordlist support and HTML/JSON/TXT reporting for deliverables.
---

# OpenDoor

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/stanislav-web/OpenDoor
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/stanislav-web/OpenDoor && cd OpenDoor && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 opendoor.py --host https://t.com` | Directory scan |
| `--wordlist /usr/share/wordlists/dirb/common.txt` | Wordlist |
| `--threads 25` | Threads |
| `--scan-dir /admin,/backup` | Specify paths |
| `--report json` | Report |

## Attack Scenario Playbook

### Directory Scanning with Multiple Reports

```bash
python3 opendoor.py --host https://t.com --threads 50 --report json
# HTML/JSON/TXT report formats, suitable for delivery
```

## Notes

A directory/admin panel scanner with multithreading and proxy support, and a complete set of report outputs.
