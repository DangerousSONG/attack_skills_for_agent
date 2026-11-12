---
name: brutespray-service-brute
description: "Brutespray: Feeds Nmap results directly into brute-force attacks. Signals: password cracking, hash cracking, SSH-only brute force, rate limiting to avoid lockout."
zh-signals: "Brutespray: Nmap 结果直通爆破。信号:密码破解,哈希破解,仅爆破 SSH,限速防锁。"
when-to-use: >-
  Use when you already have Nmap XML results and want to automatically brute-
  force the discovered services such as SSH and FTP, with rate limiting to avoid
  lockouts.
---

# Brutespray

- Attack Category: C25 Password and Hash Cracking
- Upstream Repository: https://github.com/x90skysn3k/brutespray
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install brutespray or go install github.com/x90skysn3k/brutespray@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `brutespray -f nmap.xml` | Automatically brute force every open service from the Nmap results |
| `-s ssh -u root -p pass.txt` | Brute force SSH only |
| `-c 5 -t 100` | Rate limit to avoid lockouts |
| `-o results.txt` | Output |

## Attack Scenario Playbook

### Nmap Results Straight into Brute Force

```bash
nmap -sV -oX nmap.xml 10.0.0.0/24
brutespray -f nmap.xml -u admin -p /usr/share/wordlists/top10.txt
# Automatically attacks services such as ssh/ftp/mysql/mssql
```

## Notes

Uses the Medusa engine, parses Nmap XML automatically and only brute forces open services, with a complete set of rate limiting options.
