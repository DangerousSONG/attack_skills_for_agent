---
name: subfinder-recon
description: "Enumerate subdomains passively with subfinder. Use when you need to discover the subdomains of a target domain and expand the attack surface. subfinder is ProjectDiscovery's passive subdomain discovery tool that aggregates multiple data sources such as Shodan, Censys, SecurityTrails and VirusTotal, making it fast and stealthy. This skill applies to any subdomain enumeration, attack surface discovery, or passive information gathering scenario"
zh-signals: "使用 subfinder 进行被动子域名枚举，聚合多数据源以扩展攻击面。信号:subfinder,子域名枚举,被动侦察,ProjectDiscovery,攻击面"
when-to-use: "Use when discovering subdomains of a target domain through passive sources and expanding the attack surface."
metadata:
  tags: "subfinder,subdomain,recon,subdomain enumeration,passive enumeration,information gathering,attack surface,projectdiscovery"
  category: "tool"
---

# subfinder Passive Subdomain Enumeration Methodology

subfinder is ProjectDiscovery's passive subdomain discovery tool. Core advantages: **fully passive** (generates no traffic to the target) + **multi-source aggregation** (40+ sources) + **pipeline friendly**.

Project address: https://github.com/projectdiscovery/subfinder

## Phase 1: Basic Usage

```bash
# Single domain
subfinder -d target.com

# Quiet output (only subdomains)
subfinder -d target.com -silent

# Multiple domains
subfinder -dL domains.txt -silent

# Output to file
subfinder -d target.com -o subdomains.txt
```

## Phase 2: Data Source Configuration

```bash
# Use all data sources (more comprehensive, slower)
subfinder -d target.com -all

# Specify data sources
subfinder -d target.com -s crtsh,github,shodan

# List available data sources
subfinder -ls

# Exclude specific data sources
subfinder -d target.com -es github,rapiddns
```

API key configuration: edit `~/.config/subfinder/provider-config.yaml` and add API keys to greatly improve the results.

## Phase 3: Pipeline Integration

```bash
# Subdomains → HTTP liveness detection
subfinder -d target.com -silent | httpx -silent

# Subdomains → port scan → HTTP liveness
subfinder -d target.com -silent | naabu -p 80,443 -silent | httpx -silent

# Subdomains → liveness → vulnerability scan (full chain)
subfinder -d target.com -silent | httpx -silent | nuclei -severity critical,high

# Subdomains → DNS resolution
subfinder -d target.com -silent | dnsx -a -resp -silent

# Subdomains → deduplicated IPs
subfinder -d target.com -silent | dnsx -a -resp-only -silent | sort -u
```

## Phase 4: Advanced Options

```bash
# Recursive subdomain discovery
subfinder -d target.com -recursive

# JSON output
subfinder -d target.com -json -o results.json

# Control concurrency
subfinder -d target.com -t 50

# Set the timeout
subfinder -d target.com -timeout 30

# Only show the results of specific data sources
subfinder -d target.com -cs -silent
```

## Common Scenario Quick Reference

| Scenario | Command |
|------|------|
| Quick enumeration | `subfinder -d target.com -silent` |
| Full enumeration | `subfinder -d target.com -all -silent` |
| Batch of domains | `subfinder -dL domains.txt -silent -o all_subs.txt` |
| Takeover detection chain | `subfinder -d target.com -silent \| httpx -silent \| nuclei -t takeovers/` |
