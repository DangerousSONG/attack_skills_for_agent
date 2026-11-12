---
name: autosploit-metasl
description: "AutoSploit: batch auto-exploits CVEs in authorized labs. Signals: pwn, binary exploitation, local target list, default port set"
zh-signals: "AutoSploit: 批量 CVE 自动打点(授权靶场)。信号:pwn,二进制利用,本地目标清单,默认端口集。"
when-to-use: "Use AutoSploit only in authorized lab or drill environments to batch-select targets and automatically run Metasploit exploits against identified CVEs, e.g., from a local host list or a Shodan query."
---

# AutoSploit

- Attack Category: C46 Binary Exploitation and Pwn
- Upstream Repository: https://github.com/NullArray/AutoSploit
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/NullArray/AutoSploit && cd AutoSploit && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python autosploit.py -e -q apache -c` | Search Shodan for targets and feed them to Metasploit automatically |
| `-f hosts.txt` | Local target list |
| `-p default` | Default port set |
| `--exploit-only -f x.txt` | Run exploits only against the list |

## Attack Scenario Playbook

### Batch CVE Auto-Exploitation (Authorized Labs)

```bash
python autosploit.py -e -q 'Hikvision' -c -p default
# Query Shodan → select targets → apply a Metasploit module host by host
```

## Notes

Fully automatic but noisy, with a high risk of false positives and damage; restrict it to authorized labs and drill environments.
