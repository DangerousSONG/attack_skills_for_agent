---
name: performing-bandwidth-throttling-attack-simulation
description: 'Simulate bandwidth throttling and network degradation attacks using tc,
when-to-use: 'Simulate bandwidth throttling and network degradation attacks using tc,
  iperf3, and Scapy in authorized lab environments to test QoS controls, application
  resilience, and monitoring detection of traffic manipulation. Use when validating
  how VoIP, video, or other real-time applications and network monitoring tools respond
  to degraded bandwidth or slowloris-style throttling attacks.

  '
domain: cybersecurity
subdomain: network-security
tags:
- network-security
- bandwidth-throttling
- qos
- traffic-shaping
- network-resilience
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
# Performing Bandwidth Throttling Attack Simulation

## When to Use

- Testing application resilience to degraded network conditions during authorized security assessments
- Validating QoS policies detect and mitigate unauthorized traffic shaping on the network
- Simulating network slowloris-style attacks that degrade bandwidth rather than causing complete outages
- Assessing the impact of bandwidth-based attacks on VoIP, video conferencing, and real-time applications
- Testing network monitoring tools' ability to detect abnormal bandwidth utilization patterns

**Do not use** on production networks without authorization and a maintenance window, for causing denial-of-service conditions, or against critical infrastructure without safety controls.

## Prerequisites

- Written authorization for bandwidth manipulation testing
- Linux system with tc (traffic control), netem, and iptables
- iperf3 installed on both tester and target systems for bandwidth measurement
- MITM position established (ARP spoofing) for traffic interception scenarios
- Network monitoring tools deployed for detecting the simulation
- Baseline bandwidth measurements before testing


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Workflow

### Step 1: Establish Baseline Bandwidth Measurements

```bash
# Start iperf3 server on the target
iperf3 -s -p 5201

# Measure baseline bandwidth from the tester
iperf3 -c 10.10.20.10 -t 30 -P 4 -p 5201
# Record: bandwidth, jitter, packet loss

# Measure baseline latency
ping -c 100 10.10.20.10 | tail -1
# Record: min/avg/max/mdev

# Measure baseline jitter with UDP test
iperf3 -c 10.10.20.10 -u -b 100M -t 10 -p 5201
# Record: jitter and packet loss percentage

# Document baseline values
echo "Baseline: BW=$(iperf3 -c 10.10.20.10 -t 10 -f m | tail -1 | awk '{print $7}') Mbps" > baseline.txt
echo "Latency: $(ping -c 50 10.10.20.10 | tail -1)" >> baseline.txt
```

### Step 2: Simulate Bandwidth Throttling with tc/netem

```bash
# Add traffic control to limit bandwidth on the attacker's forwarding interface
# This simulates throttling traffic flowing through a compromised router

# Limit to 1 Mbps (severe throttling)
sudo tc qdisc add dev eth0 root tbf rate 1mbit burst 32kbit latency 50ms

# Or use hierarchical token bucket for more control
sudo tc qdisc add dev eth0 root handle 1: htb default 10
sudo tc class add dev eth0 parent 1: classid 1:10 htb rate 1mbit ceil 2mbit

# Add latency and packet loss to simulate degraded link
sudo tc qdisc add dev eth0 parent 1:10 handle 10: netem delay 200ms 50ms loss 5%

# Target specific traffic (only throttle traffic to specific host)
sudo tc qdisc add dev eth0 root handle 1: htb default 99
sudo tc class add dev eth0 parent 1: classid 1:1 htb rate 1000mbit
sudo tc class add dev eth0 parent 1:1 classid 1:10 htb rate 1mbit ceil 2mbit
sudo tc class add dev eth0 parent 1:1 classid 1:99 htb rate 1000mbit

# Filter: throttle only traffic to 10.10.20.10
sudo tc filter add dev eth0 parent 1: protocol ip prio 1 u32 \
  match ip dst 10.10.20.10/32 flowid 1:10

# Verify the qdisc configuration
tc -s qdisc show dev eth0
tc -s class show dev eth0
```

### Step 3: Simulate Progressive Degradation

```bash
#!/bin/bash
# Simulate progressive bandwidth degradation over time
# This mimics an attacker slowly throttling to avoid detection

IFACE="eth0"
TARGET="10.10.20.10"

# Phase 1: Baseline (no throttling) - 5 minutes
echo "[*] Phase 1: Baseline (no throttling)"
sleep 300

# Phase 2: Mild throttling (50% reduction)
echo "[*] Phase 2: Reducing to 50 Mbps"
sudo tc qdisc add dev $IFACE root tbf rate 50mbit burst 64kbit latency 50ms
sleep 300

# Phase 3: Moderate throttling (80% reduction)
echo "[*] Phase 3: Reducing to 10 Mbps"
sudo tc qdisc change dev $IFACE root tbf rate 10mbit burst 32kbit latency 50ms
sleep 300

# Phase 4: Severe throttling + latency + loss
echo "[*] Phase 4: Reducing to 1 Mbps + 200ms latency + 5% loss"
sudo tc qdisc del dev $IFACE root 2>/dev/null
sudo tc qdisc add dev $IFACE root handle 1: htb default 10
sudo tc class add dev $IFACE parent 1: classid 1:10 htb rate 1mbit ceil 2mbit
sudo tc qdisc add dev $IFACE parent 1:10 handle 10: netem delay 200ms 50ms loss 5%
sleep 300

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
