---
name: crypthook-encrypted-tunnel
description: "CryptHook: Forwards arbitrary TCP traffic through encrypted tunnels. Signals: internal network tunneling, tunnel, encrypted listening, encrypted connection, combined use."
zh-signals: "CryptHook: 加密隧道转发任意 TCP。信号:内网穿透,隧道,加密监听,加密连接,结合使用。"
when-to-use: >-
  Use when you need to forward arbitrary TCP traffic through an AES-encrypted point-to-point
  tunnel, for example to hide C2 or pivot traffic from IDS inspection.
---

# CryptHook

- Attack Category: C32 Tunneling and Proxying
- Upstream Repository: https://github.com/chokepoint/CryptHook
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/chokepoint/CryptHook && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./crypthook -k presharedkey -l 4444` | Encrypted listener |
| `./crypthook -k key -c target.com -p 443` | Encrypted connection |
| `iptables forwarding to the target` | Combined use |
| `-d` | Daemon mode |

## Attack Scenario Playbook

### Forwarding Arbitrary TCP Through an Encrypted Tunnel

```bash
./crypthook -k secret -l 4444  # server side
./crypthook -k secret -c 10.0.0.5 -p 4444  # client side
# AES-encrypted TCP forwarding, the IDS only sees ciphertext
```

## Notes

A lightweight single-file point-to-point AES-encrypted TCP tunnel, suitable for adding an encryption layer inside an existing proxy chain.
