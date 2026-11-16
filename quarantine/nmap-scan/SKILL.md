---
name: nmap-scan
description: "Port scanning and service identification with nmap. Use when you need fine-grained port scanning, service version detection, OS fingerprinting, or NSE script-based vulnerability scanning. nmap is the most classic network scanner, supporting SYN/TCP/UDP/ACK and other scan modes, with 600+ built-in NSE scripts. Any scenario involving port scanning, service identification, vulnerability script scanning, or OS fingerprinting should use this skill. Slower than naabu, but far more capable"
zh-signals: "使用 nmap 进行端口扫描与服务识别，覆盖精细端口扫描、服务版本探测、操作系统指纹与 NSE 脚本漏洞扫描。信号:nmap,端口扫描,服务识别,NSE,操作系统指纹,版本探测"
when-to-use: "Use when you need fine-grained port scanning, service version detection, OS fingerprinting, or NSE script-based vulnerability scanning with nmap."
metadata:
  tags: "nmap,port,scan,port scanning,service identification,NSE,script scanning,OS fingerprint,SYN,TCP,UDP,version detection"
  category: "tool"
---

# nmap Port Scanning and Service Identification Methodology

nmap is the most classic network scanner. Core advantages: **service version detection** (-sV) + **the NSE script ecosystem** (600+ scripts) + **OS fingerprinting** (-O). Although slower than naabu, it is irreplaceable for deep probing.

Project address: https://nmap.org

## Tool Selection Strategy

Recommended workflow: first use naabu to quickly discover open ports, then use nmap for deep probing of the critical ports. nmap suits fine-grained scanning, not large-scale fast discovery.

Note: SYN scanning (-sS) requires root privileges; without root, TCP Connect (-sT) is used automatically.

## Phase 1: Basic Port Scanning

```bash
# SYN half-open scan (default, requires root, fastest and stealthiest)
sudo nmap -sS target.com

# TCP full connect scan (no root required)
nmap -sT target.com

# Specify the port range
nmap -p 1-1000 target.com

# Specify common ports
nmap -p 22,80,443,3306,8080 target.com

# Full port scan
nmap -p- target.com

# UDP scan (slow, requires root)
sudo nmap -sU -p 53,161,500 target.com
```

## Phase 2: Service Version and OS Identification

```bash
# Service version probing (core capability)
nmap -sV target.com

# OS fingerprinting
sudo nmap -O target.com

# Version + OS + default scripts (most common combination)
sudo nmap -A target.com

# Precise version probing (slower but more accurate)
nmap -sV --version-intensity 9 target.com
```

## Phase 3: NSE Script Scanning

```bash
# Default safe scripts
nmap -sC target.com

# Vulnerability scanning scripts
nmap --script vuln target.com

# Specific vulnerability detection
nmap --script smb-vuln-ms17-010 -p 445 target.com
nmap --script http-shellshock -p 80 target.com

# Brute force scripts
nmap --script ssh-brute -p 22 target.com
nmap --script http-brute -p 80 target.com

# HTTP information gathering
nmap --script http-title,http-headers,http-methods -p 80,443 target.com

# SMB enumeration
nmap --script smb-enum-shares,smb-enum-users -p 445 target.com

# SSL/TLS checks
nmap --script ssl-cert,ssl-enum-ciphers -p 443 target.com
```

## Phase 4: Advanced Scanning Techniques

```bash
# Bypass the firewall (fragmented packets)
sudo nmap -f target.com

# Spoof the source IP (decoy scan)
sudo nmap -D RND:5 target.com

# Specify the source port (bypass simple firewall rules)
sudo nmap --source-port 53 target.com

# Idle scan (stealthiest, requires finding a zombie host)
sudo nmap -sI zombie_host target.com

# Control the scan rate (avoid IDS)
nmap --scan-delay 1s --max-rate 10 target.com

# Timing templates (T0 is slowest and stealthiest, T5 is the fastest and most aggressive)
nmap -T4 target.com
```

## Phase 5: Output Formats

```bash
# Normal output
nmap -oN scan.txt target.com

# XML output (easy for tools to parse)
nmap -oX scan.xml target.com

# Grepable output (easy to process with grep)
nmap -oG scan.gnmap target.com

# Output all three formats at once
nmap -oA scan target.com
```

## Common Penetration Testing Combinations

| Scenario | Command |
|------|------|
| Fast full port scan | `nmap -sS -p- -T4 --open target` |
| Deep scan of known ports | `nmap -sV -sC -p 22,80,443 target` |
| Comprehensive scan | `sudo nmap -A -T4 target` |
| Vulnerability scan | `nmap --script vuln -p 80,443,445 target` |
| Internal network live host detection | `nmap -sn 10.0.0.0/24` |
| SMB vulnerability detection | `nmap --script smb-vuln* -p 445 target` |
| Web information gathering | `nmap --script http-title,http-headers -p 80,443,8080 target` |
