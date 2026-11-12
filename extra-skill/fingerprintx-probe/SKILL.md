---
name: fingerprintx-probe
description: "Use fingerprintx for application-layer service fingerprinting. Use it when you need to identify the specific service and protocol running on open ports. fingerprintx supports identification of 51 protocols (SSH/RDP/MySQL/Redis/HTTP/SMB/FTP, etc.) and outputs JSON with service metadata. Use this skill for any service identification, protocol probing, or port fingerprinting scenario."
zh-signals: "使用 fingerprintx 进行应用层服务指纹识别，支持 51 种协议并输出含元数据的 JSON。信号:服务识别,协议探测,端口指纹,fingerprintx,资产发现"
when-to-use: >-
  Use when you need to identify the specific service and protocol running on open ports
  across 51 supported protocols, and want structured JSON metadata output.
metadata:
  tags: "fingerprintx,fingerprint,probe,service-identification,protocol-probing,port-fingerprint,SSH,RDP,MySQL,Redis"
  category: "tool"
---

# fingerprintx Service Fingerprinting Methodology

fingerprintx is a service fingerprinting tool by Praetorian. Core strengths: **51 protocols** + **fast and accurate** + **JSON metadata output**.

Project URL: https://github.com/praetorian-inc/fingerprintx

## Phase 1: Basic Usage

```bash
# Single target
fingerprintx -t 192.168.1.1:22

# Multiple targets
fingerprintx -t 192.168.1.1:22,192.168.1.1:80,192.168.1.1:443

# Read from a file (host:port format)
fingerprintx -l targets.txt

# Read from stdin
echo "192.168.1.1:80" | fingerprintx
```

## Phase 2: Scan Modes

```bash
# Fast mode (only tries the default service of each port)
fingerprintx -t 192.168.1.1:22 --fast

# UDP service probing
fingerprintx -t 192.168.1.1:161 -U

# Set timeout
fingerprintx -t 192.168.1.1:22 -w 1000

# JSON output
fingerprintx -t 192.168.1.1:22 --json
```

## Phase 3: Pipeline Integration

```bash
# naabu port scan -> service identification
naabu -host 192.168.1.0/24 -silent | fingerprintx

# masscan -> service identification
sudo masscan 10.0.0.0/24 -p 22,80,443 -oL - | \
  grep "^open" | awk '{print $4":"$3}' | fingerprintx --json
```
