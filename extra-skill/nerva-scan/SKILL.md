---
name: nerva-scan
description: "Use nerva for high-performance service fingerprinting. Use it when you need to identify the specific service on open ports. nerva supports 120+ protocols (databases, remote access, message queues, ICS, web, etc.) and is an upgraded version of fingerprintx. Use this skill for any service identification, protocol probing, or port fingerprinting scenario."
zh-signals: "使用 nerva 进行高性能服务指纹识别与协议探测。信号:服务识别,协议探测,端口指纹,nerva,120+协议"
when-to-use: "Use when you need to identify services on open ports, fingerprint 120+ protocols (databases, remote access, message queues, ICS, web), or run TCP/UDP/SCTP probes."
metadata:
  tags: "nerva,fingerprint,scan,service-identification,protocol-probing,port-fingerprint,120+protocols,ICS,database"
  category: "tool"
---

# nerva High-Performance Service Fingerprinting Methodology

nerva is a service fingerprinting tool by Praetorian (an upgraded version of fingerprintx). Core strengths: **120+ protocols** + **TCP/UDP/SCTP multi-transport** + **rich metadata extraction**.

Project URL: https://github.com/praetorian-inc/nerva

## Phase 1: Basic Usage

```bash
# Single target
nerva -t 192.168.1.1:22

# Multiple targets
nerva -t 192.168.1.1:22,192.168.1.1:80,192.168.1.1:3306

# Read from a file
nerva -l targets.txt

# JSON output
nerva -t 192.168.1.1:22 --json
```

## Phase 2: Scan Modes

```bash
# Fast mode (only tries default services)
nerva -t 192.168.1.1:22 --fast

# UDP probing
nerva -t 192.168.1.1:161 -U

# Set timeout and concurrency
nerva -t targets -w 2000 -W 50

# Rate limiting
nerva -l targets.txt -R 100
```

## Phase 3: Pipeline Integration

```bash
# naabu port scan -> service identification
naabu -host 192.168.1.0/24 -silent | nerva --json

# masscan -> service identification
sudo masscan 10.0.0.0/24 -p 1-10000 -oL - | \
  grep "^open" | awk '{print $4":"$3}' | nerva --json -o services.json
```
