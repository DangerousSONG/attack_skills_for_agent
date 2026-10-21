---
name: performing-external-network-penetration-test
description: Conduct a comprehensive external network penetration test to identify
when-to-use: Conduct a comprehensive external network penetration test to identify
  vulnerabilities in internet-facing infrastructure using PTES methodology, reconnaissance,
  scanning, exploitation, and reporting.
domain: cybersecurity
subdomain: penetration-testing
tags:
- external-pentest
- network-security
- PTES
- OSSTMM
- Nmap
- Metasploit
- vulnerability-assessment
- reconnaissance
- exploitation
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-06
- GV.OV-02
- DE.AE-07
mitre_attack:
- T1595
- T1190
- T1059
- T1078
- T1592
---

# Performing External Network Penetration Test

## Overview

An external network penetration test simulates a real-world attacker targeting an organization's internet-facing assets such as firewalls, web servers, mail servers, DNS servers, VPN gateways, and cloud endpoints. The objective is to identify exploitable vulnerabilities before malicious actors do, following frameworks like PTES (Penetration Testing Execution Standard), OSSTMM, and NIST SP 800-115.


## When to Use

- When conducting security assessments that involve performing external network penetration test
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Written authorization (Rules of Engagement document signed by asset owner)
- Defined scope: IP ranges, domains, subdomains, and exclusions
- Testing environment: Kali Linux or Parrot OS with updated tools
- VPN/dedicated testing infrastructure to avoid IP blocks
- Coordination with SOC/NOC for timing windows

## Phase 1 — Pre-Engagement and Scoping

### Define Rules of Engagement

```
Scope:
  - Target IP ranges: 203.0.113.0/24, 198.51.100.0/24
  - Domains: *.target.com, *.target.io
  - Exclusions: 203.0.113.50 (production DB), *.staging.target.com
  - Testing window: Mon-Fri 22:00-06:00 UTC
  - Emergency contact: SOC Lead — +1-555-0100
  - Authorization ID: PENTEST-2025-EXT-042
```

### Legal Documentation Checklist

| Document | Status | Owner |
|----------|--------|-------|
| Master Service Agreement (MSA) | Signed | Legal |
| Statement of Work (SOW) | Signed | PM |
| Rules of Engagement (RoE) | Signed | CISO |
| Get-Out-of-Jail Letter | Signed | CTO |
| NDA | Signed | Legal |
| Insurance Certificate | Verified | Risk |

## Phase 2 — Reconnaissance (Information Gathering)

### Passive Reconnaissance

```bash
# OSINT — Subdomain enumeration
subfinder -d target.com -o subdomains.txt
amass enum -passive -d target.com -o amass_subs.txt
cat subdomains.txt amass_subs.txt | sort -u > all_subs.txt

# DNS record enumeration
dig target.com ANY +noall +answer
dig target.com MX +short
dig target.com NS +short
dig target.com TXT +short

# WHOIS and ASN lookup
whois target.com
whois -h whois.radb.net -- '-i origin AS12345'

# Certificate Transparency log search
curl -s "https://crt.sh/?q=%.target.com&output=json" | jq '.[].name_value' | sort -u

# Google dorking
# site:target.com filetype:pdf
# site:target.com inurl:admin
# site:target.com intitle:"index of"

# Shodan enumeration
shodan search "org:Target Corp" --fields ip_str,port,product
shodan host 203.0.113.10

# Email harvesting
theHarvester -d target.com -b all -l 500 -f theharvester_results

# GitHub/GitLab secret scanning
trufflehog github --org=targetcorp --concurrency=5
gitleaks detect --source=https://github.com/targetcorp/repo
```

### Active Reconnaissance

```bash
# Host discovery — ping sweep
nmap -sn 203.0.113.0/24 -oG ping_sweep.gnmap

# TCP SYN scan — top 1000 ports
nmap -sS -sV -O -T4 203.0.113.0/24 -oA tcp_scan

# Full TCP port scan
nmap -sS -p- -T4 --min-rate 1000 203.0.113.0/24 -oA full_tcp

# UDP scan — top 100 ports
nmap -sU --top-ports 100 -T4 203.0.113.0/24 -oA udp_scan

# Service version and script scan
nmap -sV -sC -p 21,22,25,53,80,110,143,443,445,993,995,3389,8080,8443 203.0.113.0/24 -oA service_scan

# SSL/TLS enumeration
sslscan 203.0.113.10:443
testssl.sh --full https://target.com

# Web technology fingerprinting
whatweb -v https://target.com
wappalyzer https://target.com
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
