---
name: performing-web-application-scanning-with-nikto
description: "Runs Nikto web server and application scanner. Signals: web scanning, vulnerability scanning, Burp."
zh-signals: "Runs Nikto, an open-source web server and web application scanner 信号:web扫描,漏洞扫描,burp。"
when-to-use: Runs Nikto, an open-source web server and web application scanner,
  to test over 7,000 potentially dangerous files/programs, check for outdated versions
  across 1,250+ servers, and identify XSS, SQL injection, misconfigurations, default
  credentials, and vulnerable CGI scripts. Use when performing web application vulnerability
  scanning, security assessments, scheduled security testing, or validating web
  server security controls.
domain: cybersecurity
subdomain: vulnerability-management
tags:
- vulnerability-management
- cve
- nikto
- web-scanning
- owasp
- risk
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- ID.RA-01
- ID.RA-02
- ID.IM-02
- ID.RA-06
mitre_attack:
- T1190
- T1203
- T1068
---
# Performing Web Application Scanning with Nikto

## Overview
Nikto is an open-source web server and web application scanner that tests against over 7,000 potentially dangerous files/programs, checks for outdated versions of over 1,250 servers, and identifies version-specific problems on over 270 servers. It performs comprehensive tests including XSS, SQL injection, server misconfigurations, default credentials, and known vulnerable CGI scripts.


## When to Use

- When conducting security assessments that involve performing web application scanning with nikto
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites
- Nikto installed (Perl-based, included in Kali Linux)
- Written authorization to scan target web servers
- Network access to target web applications
- Understanding of HTTP/HTTPS protocols

## Core Concepts

### What Nikto Detects
- Server misconfigurations and dangerous default files
- Outdated server software versions with known CVEs
- Common CGI vulnerabilities and dangerous scripts
- Default credentials and admin pages
- HTTP methods that should be disabled (PUT, DELETE, TRACE)
- SSL/TLS misconfigurations and weak ciphers
- Missing security headers (X-Frame-Options, CSP, HSTS)
- Information disclosure through headers and error pages

### Nikto vs Other Web Scanners
| Feature | Nikto | OWASP ZAP | Burp Suite | Nuclei |
|---------|-------|-----------|------------|--------|
| License | Open Source | Open Source | Commercial | Open Source |
| Focus | Server/Config | App Logic | Full Pentest | Template-Based |
| Speed | Fast | Medium | Slow | Very Fast |
| False Positives | Moderate | Low | Low | Low |
| Authentication | Basic | Full | Full | Template |
| Active Community | Yes | Yes | Yes | Yes |

## Workflow

### Step 1: Basic Scanning
```bash
# Basic scan against a target
nikto -h https://target.example.com

# Scan specific port
nikto -h target.example.com -p 8443

# Scan multiple ports
nikto -h target.example.com -p 80,443,8080,8443

# Scan with SSL enforcement
nikto -h target.example.com -ssl

# Scan from a host list file
nikto -h targets.txt
```

### Step 2: Advanced Scanning Options
```bash
# Comprehensive scan with all tuning options
nikto -h https://target.example.com \
  -Tuning 123456789abcde \
  -timeout 10 \
  -Pause 2 \
  -Display V \
  -output report.html \
  -Format htm

# Tuning options control test types:
# 0 - File Upload
# 1 - Interesting File / Seen in logs
# 2 - Misconfiguration / Default File
# 3 - Information Disclosure
# 4 - Injection (XSS/Script/HTML)
# 5 - Remote File Retrieval - Inside Web Root
# 6 - Denial of Service
# 7 - Remote File Retrieval - Server Wide
# 8 - Command Execution / Remote Shell
# 9 - SQL Injection
# a - Authentication Bypass
# b - Software Identification
# c - Remote Source Inclusion
# d - WebService
# e - Administrative Console

# Scan with specific tuning (XSS + SQL injection + auth bypass)
nikto -h https://target.example.com -Tuning 49a

# Scan with authentication
nikto -h https://target.example.com -id admin:password

# Scan through a proxy
nikto -h https://target.example.com -useproxy http://proxy:8080

# Scan with custom User-Agent
nikto -h https://target.example.com -useragent "Mozilla/5.0 (Security Scan)"

# Scan specific CGI directories
nikto -h https://target.example.com -Cgidirs /cgi-bin/,/scripts/

# Evasion techniques (IDS avoidance for authorized testing)
# 1-Random URI encoding, 2-Directory self-reference
# 3-Premature URL ending, 4-Prepend long random string
nikto -h https://target.example.com -evasion 1234
```

### Step 3: Output and Reporting
```bash
# Generate multiple output formats
nikto -h https://target.example.com -output scan.csv -Format csv
nikto -h https://target.example.com -output scan.xml -Format xml
nikto -h https://target.example.com -output scan.html -Format htm
nikto -h https://target.example.com -output scan.txt -Format txt

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
