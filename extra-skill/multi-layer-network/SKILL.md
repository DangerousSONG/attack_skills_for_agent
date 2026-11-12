---
name: multi-layer-network
description: "Multi-layer network penetration and tunnel setup. Use when pivoting from a DMZ foothold into the internal network, penetrating across network segments, or when the target sits behind multiple firewalls and network zones. Covers proxy setup (frp/chisel/SSH), multi-hop tunnel chains, port forwarding, and SOCKS proxies. The complete multi-layer attack path from perimeter breach to domain controller"
zh-signals: "多层网络渗透与隧道搭建，从 DMZ 立足点穿透防火墙进入内网。信号:内网穿透,隧道,代理,frp,chisel,横向移动"
when-to-use: >-
  Use when pivoting from a DMZ foothold across network segments, or when the target sits
  behind multiple firewalls and requires tunnels, port forwarding, or SOCKS proxies.
metadata:
  tags: "pivot,proxy,tunnel,multi-layer,lateral,tunneling,proxy,port-forwarding,frp,chisel,ssh,socks,internal-network-pivoting,pivot-host,DMZ"
  category: "lateral"
---

# Multi-Layer Network Penetration Methodology

## ⛔ Further Reading (Must Read)

- frp/chisel/Neo-reGeorg/SSH tunnel configuration commands, multi-hop proxy chains, proxychains usage → [references/tunnel-tools.md](references/tunnel-tools.md)

---

## Phase 1: Perimeter Breach and Foothold

Once you have a shell on a DMZ host, collect network information immediately:
```bash
ip addr && ip route && arp -a && cat /etc/hosts      # Linux
ipconfig /all && route print && arp -a                 # Windows
```

**Key Decision**:
- Dual NICs (eth0=external, eth1=10.x.x.x) → a natural pivot
- Internal IP only → set up a reverse tunnel

### Target Network Mapping
```bash
for i in $(seq 1 254); do ping -c 1 -W 1 10.0.0.$i &>/dev/null && echo "10.0.0.$i alive"; done
fscan -h 10.0.0.0/24 -nopoc
```

## Phase 2: Tunnel Selection Decision Tree

```
Can the target reach the Internet?
├─ Outbound access available (external network reachable)
│   ├─ SSH credentials available? → SSH -D 1080 (zero deployment, simplest)
│   ├─ Need long-term stability? → frp (auto-reconnect)
│   └─ Need rapid deployment? → chisel (single binary)
├─ HTTP-only outbound → Neo-reGeorg HTTP tunnel
└─ No outbound access at all → SSH reverse tunnel / relay through the pivot host
```

See → [references/tunnel-tools.md](references/tunnel-tools.md) for the detailed configuration commands of every tool

## Tunnel Tool Selection Quick Reference

| Scenario | Recommended Tool | Rationale |
|------|----------|------|
| SSH credentials available | SSH tunnel | Zero deployment, simplest |
| Outbound access + long-term use | frp | Most stable, supports auto-reconnect |
| Outbound access + rapid deployment | chisel | Single binary, no config file |
| HTTP-only outbound | Neo-reGeorg | HTTP tunnel crosses firewalls |
| High performance required | ligolo-ng | TUN interface, near-native performance |

## Phase 3: Deep Penetration

Once you are inside the internal network through the proxy, proceed in priority order:
1. **Internal network reconnaissance**
2. **Domain environment attacks**
3. **Credential spraying**
4. **Lateral movement**

## Notes
- **proxychains only supports TCP**, not ICMP (ping is unavailable, use `-Pn -sT` with nmap)
- After the tunnel is established, test connectivity with `proxychains curl` before running large-scale scans
- Tunnel processes break easily — use `autossh` or frp auto-reconnect to keep them stable
- Record the credentials and tunnel command for every hop so the path can be rebuilt

## Proxychains Limitations
- No UDP support: proxychains only proxies TCP, so UDP scans (-sU) will fail
