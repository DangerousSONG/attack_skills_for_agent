---
name: internal-recon
description: "Internal network information gathering and topology mapping. Use after breaching the perimeter and gaining an internal foothold. Covers live host discovery, port scanning, service identification, and critical infrastructure location (domain controller / database / mail / file server). The first step of an internal penetration test — see the map clearly before acting"
zh-signals: "内网信息收集与拓扑绘制，覆盖存活探测、端口扫描、服务识别与高价值目标定位。信号:内网侦察,存活探测,端口扫描,域控定位,拓扑绘制"
when-to-use: "Use after gaining an internal foothold past the perimeter, to discover live hosts, scan ports, identify services, and locate domain controllers, databases, mail, and file servers."
metadata:
  tags: "internal,recon,network,discovery,internal-network,reconnaissance,topology,live-host-detection,port-scanning,domain-controller"
  category: "lateral"
---

# Internal Network Reconnaissance Methodology

How internal reconnaissance differs from external reconnaissance: internal networks usually have no CDN/WAF protection, but your operating space is constrained by the network position of your current foothold. The core goal is to **map the internal network quickly** — which hosts exist, what services they run, and which are high-value targets.

## ⛔ Further Reading (Must Read)

- Live host detection commands, port → service → value mapping table, domain controller / database location → [references/network-mapping.md](references/network-mapping.md)
- Detailed fscan usage (weak credential brute-forcing, POC detection, proxy scanning) → load the `fscan-scan` skill
- **Tool delivery methods** (how to transfer post-exploitation tools to the target, and why to execute them on the target instead of locally) → load the `tool-delivery` skill

## Phase 1: Current Position Analysis

```bash
# Linux
ip addr && ip route && cat /etc/resolv.conf && arp -a && cat /etc/hosts
# Windows
ipconfig /all && route print && arp -a && net view /domain
```

**Key indicators**: multiple NICs = pivot | DNS resolving to internal IPs = domain environment | large ARP table = active network segment

## Phase 2: Live Host Discovery (fscan first)
```bash
# fscan all-in-one (live hosts + ports + services + weak credentials + vulnerabilities, far faster than nmap)
fscan -h 10.0.0.0/24 -nopoc          # quick live host + port scan
fscan -h 10.0.0.0/24                  # full scan (includes POC detection + weak credentials)

# nmap fallback (degrade when fscan is unavailable)
nmap -sn 10.0.0.0/24                  # ICMP ping
nmap -PR -sn 10.0.0.0/24             # ARP (most reliable on the same subnet)
```

## Phase 3: Port Scanning (focus on critical ports)
```bash
# fscan with explicit ports (recommended, fast and auto-identifies services)
fscan -h TARGETS -p 22,80,135,139,443,445,1433,3306,3389,5432,5985,6379,8080,9200

# nmap deep identification (use when service versions / NSE scripts are needed)
nmap -sT -sV -p 22,80,445,3389 TARGETS
```

**High-value ports**: 88(domain controller) | 445(SMB) | 3389(RDP) | 1433(MSSQL) | 6379(Redis)

→ Full port → service → value mapping table → [references/network-mapping.md](references/network-mapping.md)

## Phase 4: Critical Infrastructure Location

- **Domain controller**: 88+389+445 = confirmed DC | the DNS IP is usually the domain controller
- **Databases**: try connecting with the credentials you have collected
- **Management systems**: `httpx -tech-detect` / `curl -sI` to find Jenkins/GitLab/Zabbix

## Phase 5: Output the Internal Network Map
Network topology + high-value target list (domain controller → database → management system → pivot host) + priority attack paths

## Notes
- Prefer **passive discovery** (ARP/routing table) first, then active scanning
- Scan in batches to avoid taking down the network with a /16 sweep

## Passive Discovery Techniques
- NBNS / LLMNR broadcast listening: NetBIOS name services leak hostnames passively
- tcpdump packet capture, listening, and network traffic sniffing
- Port 3268 — Active Directory Global Catalog

## Multi-NIC Pivoting
- Find dual-NIC hosts (two subnets) — they can serve as cross-subnet pivot hosts
- Set up proxies/forwarding through such a machine to reach new subnets
- New attack surface: expand the scope, go deeper into the internal network
