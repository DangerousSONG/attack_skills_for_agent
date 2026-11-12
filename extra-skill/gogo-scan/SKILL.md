---
name: gogo-scan
description: "Perform port scanning and fingerprinting with gogo. gogo is a high-speed port scanner by chainreactors that supports active/passive fingerprinting, structured group output, and automatic certificate extraction via the TLS handshake. Difference from fscan: gogo focuses on scan precision and fingerprint coverage (2000+ fingerprint rules), while fscan also handles weak credentials and POCs. Prefer gogo when you need to accurately identify target services and middleware versions (not just open ports). Consider this skill for port scanning, service identification, fingerprinting, and asset discovery scenarios"
zh-signals: "使用 gogo 进行高速端口扫描与指纹识别，内置 2000+ 指纹规则并输出结构化结果。信号:端口扫描,指纹识别,gogo,资产发现,服务识别"
when-to-use: >-
  Use when you need accurate port scanning and service/middleware fingerprinting with
  2000+ fingerprint rules, prioritizing precision over password or POC scanning.
metadata:
  tags: "gogo,port,scan,fingerprint,fingerprinting,port,scanning,asset discovery,chainreactors"
  category: "tool"
---

# gogo High-Speed Port Scanning and Fingerprinting

The core advantage of gogo is **fingerprint precision** - it ships with 2000+ fingerprint rules that accurately identify web frameworks, middleware versions and CMS types, and outputs structured JSON for downstream processing.

Project address: https://github.com/chainreactors/gogo

## Basic Usage

```bash
# Scan a single target
gogo -i 10.0.0.1

# Scan a network segment
gogo -i 10.0.0.0/24

# Scan the specified ports
gogo -i 10.0.0.0/24 -p 80,443,8080,8443

# Scan the Top1000 ports
gogo -i 10.0.0.0/24 -p top1000

# Read targets from a file
gogo -l targets.txt
```

## Output Control

```bash
# JSON output (easy to process downstream)
gogo -i 10.0.0.0/24 -o result.json -f json

# Only output live hosts that have fingerprints
gogo -i 10.0.0.0/24 --filter

# CSV output
gogo -i 10.0.0.0/24 -o result.csv -f csv
```

## Advanced Scanning

```bash
# Adjust concurrency (500 by default, can be raised on an internal network)
gogo -i 10.0.0.0/16 -t 2000

# Enable version probing (more precise but slower)
gogo -i 10.0.0.1 -p top1000 -v

# Specify the timeout (milliseconds)
gogo -i 10.0.0.0/24 --timeout 3000

# Exclude ports
gogo -i 10.0.0.0/24 --exclude-port 22,80
```

## Integration with Other Tools

```bash
# gogo discovers services → nuclei scans for vulnerabilities
gogo -i 10.0.0.0/24 -p top1000 -o result.json -f json
cat result.json | jq -r '.[] | select(.port==80 or .port==443 or .port==8080) | .uri' | nuclei -t ~/nuclei-templates/

# gogo discovers services → httpx probes them
gogo -i 10.0.0.0/24 -o result.json -f json
cat result.json | jq -r '.uri' | httpx -silent
```

## Decision Tree

```
What do you need to scan?
├─ Quick look at segment liveness + weak credentials + POCs → fscan
├─ Precise fingerprinting (web framework / CMS / middleware versions) → gogo
├─ Large-scale port scanning (SYN / full port range) → naabu or nmap
└─ Subdomain assets → subfinder + httpx
```
