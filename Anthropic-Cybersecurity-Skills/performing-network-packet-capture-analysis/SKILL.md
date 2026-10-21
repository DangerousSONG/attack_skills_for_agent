---
name: performing-network-packet-capture-analysis
description: Perform forensic analysis of network packet captures (PCAP/PCAPNG) using Wireshark, tshark, and tcpdump to reconstruct network communications, extract transferred files, identify malicious traffic, and establish evidence of data exfiltration or command-and-control activity. Use when a PCAP file from an incident needs to be examined to prove lateral movement, malware delivery, or unauthorized access.
when-to-use: Perform forensic analysis of network packet captures (PCAP/PCAPNG) using Wireshark, tshark, and tcpdump to reconstruct network communications, extract transferred files, identify malicious traffic, an
domain: cybersecurity
subdomain: digital-forensics
tags:
- pcap
- wireshark
- tshark
- tcpdump
- network-forensics
- packet-capture
- protocol-analysis
- traffic-analysis
- pcapng
- network-evidence
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- RS.AN-03
- DE.AE-02
- RS.MA-01
mitre_attack:
- T1005
- T1074
- T1119
- T1070
- T1048
---

# Performing Network Packet Capture Analysis

## Overview

Network packet captures (PCAP/PCAPNG files) represent the ultimate source of truth about network activity and provide irrefutable evidence of communications between hosts. PCAP files log every packet transmitted over a network segment, making them vital for forensic investigations involving data exfiltration, command-and-control communications, lateral movement, malware delivery, and unauthorized access. Wireshark is the primary tool for interactive analysis, while tshark provides command-line capabilities for automated processing and scripting. Modern PCAPNG format supports additional metadata including interface descriptions, capture comments, precise timestamps, and per-packet annotations.


## When to Use

- When conducting security assessments that involve performing network packet capture analysis
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Wireshark 4.x with protocol dissectors
- tshark command-line tool (included with Wireshark)
- tcpdump for capture and basic filtering
- Python 3.8+ with scapy and pyshark libraries
- Sufficient disk space for PCAP files (can be multi-GB)

## Capture Techniques

### tcpdump

```bash
# Capture all traffic on interface eth0
tcpdump -i eth0 -w capture.pcap

# Capture with rotation (100MB files, keep 10)
tcpdump -i eth0 -w capture_%Y%m%d_%H%M%S.pcap -C 100 -W 10

# Capture specific host traffic
tcpdump -i eth0 host 192.168.1.100 -w host_traffic.pcap

# Capture specific port traffic
tcpdump -i eth0 port 443 -w https_traffic.pcap

# Capture with BPF filter for suspicious ports
tcpdump -i eth0 'port 4444 or port 8080 or port 1337' -w suspicious.pcap
```

### Wireshark Display Filters

```
# HTTP traffic
http

# DNS queries
dns

# SMB file transfers
smb2

# Specific IP communication
ip.addr == 192.168.1.100

# Failed TCP connections
tcp.flags.syn == 1 && tcp.flags.ack == 0

# Large data transfers (potential exfiltration)
tcp.len > 1000

# Specific protocol by port
tcp.port == 4444

# TLS handshakes (SNI extraction)
tls.handshake.type == 1

# HTTP POST requests
http.request.method == "POST"

# DNS queries to suspicious TLDs
dns.qry.name contains ".xyz" or dns.qry.name contains ".top"

# Beaconing detection (regular intervals)
frame.time_delta_displayed > 55 && frame.time_delta_displayed < 65
```

### tshark Analysis Commands

```bash
# Extract HTTP URLs from capture
tshark -r capture.pcap -Y "http.request" -T fields -e http.host -e http.request.uri

# Extract DNS queries
tshark -r capture.pcap -Y "dns.flags.response == 0" -T fields -e dns.qry.name | sort -u

# Extract file transfers (HTTP objects)
tshark -r capture.pcap --export-objects http,exported_files/

# Extract SMB file transfers
tshark -r capture.pcap --export-objects smb,smb_files/

# Protocol hierarchy statistics
tshark -r capture.pcap -z io,phs

# Conversation statistics
tshark -r capture.pcap -z conv,tcp

# Extract TLS SNI (Server Name Indication)
tshark -r capture.pcap -Y "tls.handshake.type == 1" -T fields -e tls.handshake.extensions_server_name

# Top talkers by bytes
tshark -r capture.pcap -z endpoints,ip -q

# Extract credentials (FTP, HTTP Basic)
tshark -r capture.pcap -Y "ftp.request.command == USER || ftp.request.command == PASS || http.authorization" -T fields -e ftp.request.arg -e http.authorization
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
