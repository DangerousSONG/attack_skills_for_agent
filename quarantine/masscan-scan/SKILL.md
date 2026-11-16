---
name: masscan-scan
description: "Ultra-large-scale high-speed port scanning with masscan. Use when scanning large CIDR ranges or internet-scale targets. masscan is an asynchronous stateless scanner that can reach millions of packets per second, making it ideal for large-scale asset discovery. Requires root privileges. Use this skill for any scenario involving large-scale network segment scanning, high-speed port discovery, or internet-wide mapping"
zh-signals: "使用 masscan 进行超大规模高速端口扫描与资产发现。信号:端口扫描,masscan,大规模扫描,CIDR,资产发现"
when-to-use: >-
  Use when scanning large CIDR ranges or internet-scale targets at very high packet rates and root privileges are available.
metadata:
  tags: "masscan,port,scan,port scanning,high-speed scanning,large-scale,CIDR,network segment,asset discovery,asynchronous scanning"
  category: "tool"
---

# masscan Ultra-Large-Scale High-Speed Port Scanning Methodology

masscan is an asynchronous stateless port scanner. Core advantages: **extreme speed** (theoretically up to 10 million packets/second) + **large-scale scanning** (designed for full-internet scans) + **nmap-compatible output**. Requires root privileges.

Project URL: https://github.com/robertdavidgraham/masscan

## Tool Selection Strategy

masscan is suited to large network segments (/16 and larger) and is far faster than nmap and naabu. However, it does not perform service identification. Recommended workflow: masscan for fast port discovery → nmap -sV for service identification. naabu is more convenient for small-range scans.

## Phase 1: Basic Scanning

```bash
# Scan a single target (requires root)
sudo masscan 192.168.1.1 -p 80,443,8080

# Scan a network segment
sudo masscan 10.0.0.0/24 -p 1-1000

# Full port scan
sudo masscan 192.168.1.0/24 -p 0-65535

# Control the packet rate (default 100 packets/second)
sudo masscan 10.0.0.0/16 -p 80,443 --rate 10000
```

## Phase 2: Large-Scale Scanning

```bash
# /16 scan (65536 IPs)
sudo masscan 10.0.0.0/16 -p 22,80,443,3389 --rate 50000

# /8 scan (use with caution)
sudo masscan 10.0.0.0/8 -p 80,443 --rate 100000

# Read targets from a file
sudo masscan -iL targets.txt -p 80,443

# Exclude specific IPs
sudo masscan 10.0.0.0/16 -p 80 --excludefile exclude.txt
```

## Phase 3: Output Formats

```bash
# List format (concise, recommended)
sudo masscan 10.0.0.0/24 -p 80,443 -oL results.txt

# JSON format
sudo masscan 10.0.0.0/24 -p 80,443 -oJ results.json

# nmap XML format (compatible with the nmap toolchain)
sudo masscan 10.0.0.0/24 -p 80,443 -oX results.xml

# Grepable format
sudo masscan 10.0.0.0/24 -p 80,443 -oG results.gnmap
```

## Phase 4: Advanced Options

```bash
# Banner grabbing
sudo masscan 10.0.0.0/24 -p 80 --banners

# Specify the network interface
sudo masscan 10.0.0.0/24 -p 80 -e eth0

# Specify the source IP
sudo masscan 10.0.0.0/24 -p 80 --adapter-ip 192.168.1.100

# Pause and resume a scan
sudo masscan 10.0.0.0/8 -p 80 --resume paused.conf
# Ctrl+C generates paused.conf when pausing

# Use a configuration file
sudo masscan -c masscan.conf
```

## Common Penetration Testing Combinations

| Scenario | Command |
|------|------|
| Fast internal network discovery | `sudo masscan 10.0.0.0/16 -p 22,80,443,3389 --rate 10000 -oL results.txt` |
| Web service discovery | `sudo masscan CIDR -p 80,443,8080,8443 --rate 50000 -oL web.txt` |
| Database ports | `sudo masscan CIDR -p 3306,5432,1433,6379,27017 --rate 10000` |
| Full port scan | `sudo masscan target -p 0-65535 --rate 10000 -oL all.txt` |
