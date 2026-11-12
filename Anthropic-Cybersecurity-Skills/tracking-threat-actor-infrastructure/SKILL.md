---
name: tracking-threat-actor-infrastructure
description: "Discovers and maps adversary-controlled C2 infrastructure. Signals: C2, command and control, remote control."
zh-signals: "Discovers and maps adversary-controlled infrastructure (C2 servers) 信号:c2,命令控制,远控。"
when-to-use: Discovers and maps adversary-controlled infrastructure (C2 servers,
  phishing domains, exploit-kit hosts, bulletproof hosting) by pivoting across passive
  DNS, certificate transparency logs, Shodan/Censys scans, WHOIS records, and network
  fingerprints (JARM/JA3S). Use when tracking threat actor infrastructure, expanding
  a known IOC into related assets, or producing STIX-based threat intelligence during
  a CTI investigation.
domain: cybersecurity
subdomain: threat-intelligence
tags:
- threat-intelligence
- cti
- ioc
- mitre-attack
- stix
- infrastructure-tracking
- shodan
- censys
- passive-dns
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-05
- DE.CM-01
- DE.AE-02
mitre_attack:
- T1591
- T1592
- T1593
- T1589
- T1566
mitre_f3:
  version: '1.1'
  tactics:
  - reconnaissance
  - resource-development
  techniques:
  - id: T1593
    name: Search Open Websites/Domains
    tactic: reconnaissance
    source: attack
  - id: T1583.001
    name: 'Acquire Infrastructure: Domains'
    tactic: resource-development
    source: attack
  - id: T1583.008
    name: 'Acquire Infrastructure: Malvertising'
    tactic: resource-development
    source: attack
  - id: T1583.003
    name: 'Acquire Infrastructure: Virtual Private Network or Server'
    tactic: resource-development
    source: attack
  - id: F1020.002
    name: 'Create Fake Materials: Fake Website'
    tactic: resource-development
    source: f3
  - id: T1608.006
    name: 'Stage Capabilities: SEO Poisoning'
    tactic: resource-development
    source: attack
---
# Tracking Threat Actor Infrastructure

## Overview

Threat actor infrastructure tracking involves monitoring and mapping adversary-controlled assets including command-and-control (C2) servers, phishing domains, exploit kit hosts, bulletproof hosting, and staging servers. This skill covers using passive DNS, certificate transparency logs, Shodan/Censys scanning, WHOIS analysis, and network fingerprinting to discover, track, and pivot across threat actor infrastructure over time.


## When to Use

- When managing security operations that require tracking threat actor infrastructure
- When improving security program maturity and operational processes
- When establishing standardized procedures for security team workflows
- When integrating threat intelligence or vulnerability data into operations

## Prerequisites

- Python 3.9+ with `shodan`, `censys`, `requests`, `stix2` libraries
- API keys: Shodan, Censys, VirusTotal, SecurityTrails, PassiveTotal
- Understanding of DNS, TLS/SSL certificates, IP allocation, ASN structure
- Familiarity with passive DNS and certificate transparency concepts
- Access to domain registration (WHOIS) lookup services

## Key Concepts

### Infrastructure Pivoting
Pivoting is the technique of using one known indicator to discover related infrastructure. Starting from a known C2 IP address, analysts can pivot via: passive DNS (find domains), reverse WHOIS (find related registrations), SSL certificates (find shared certs), SSH key fingerprints, HTTP response fingerprints, JARM/JA3S hashes, and WHOIS registrant data.

### Passive DNS
Passive DNS databases record DNS query/response data observed at recursive resolvers. This allows analysts to find historical domain-to-IP mappings, discover domains hosted on a known C2 IP, and identify fast-flux or domain generation algorithm (DGA) behavior.

### Certificate Transparency
Certificate Transparency (CT) logs publicly record all SSL/TLS certificates issued by CAs. Monitoring CT logs reveals new certificates registered for suspicious domains, helping identify phishing sites and C2 infrastructure before they become active.

### Network Fingerprinting
- **JARM**: Active TLS server fingerprint (hash of TLS handshake responses)
- **JA3S**: Passive TLS server fingerprint (hash of Server Hello)
- **HTTP Headers**: Server banners, custom headers, response patterns
- **Favicon Hash**: Hash of HTTP favicon for server identification

## Workflow

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.
