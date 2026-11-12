---
name: ksubdomain-brute
description: "Use ksubdomain for stateless subdomain brute-forcing. Use it when you need extremely fast subdomain brute-forcing and validation. ksubdomain sends packets directly through raw sockets on the network interface, making it 10x faster than dnsx, and supports both validation and enumeration modes. Requires root privileges. Use this skill for any high-speed subdomain brute-forcing or large-scale subdomain validation scenario."
zh-signals: "使用 ksubdomain 进行无状态高速子域名爆破与验证。信号:子域名爆破,ksubdomain,DNS枚举,资产测绘"
when-to-use: >-
  Use when you need extremely fast subdomain brute-forcing or large-scale subdomain
  validation and have root privileges for raw-socket packet sending.
metadata:
  tags: "ksubdomain,subdomain,brute,subdomain-bruteforce,stateless,high-speed,DNS,validation,enumeration"
  category: "tool"
---

# ksubdomain Stateless Subdomain Brute-Forcing Methodology

ksubdomain is a stateless subdomain brute-forcing tool. Core strengths: **extreme speed** (raw-socket packet sending, 10x faster than dnsx) + **dual validation/enumeration modes** + **bandwidth control**. Requires root privileges.

Project URL: https://github.com/boy-hack/ksubdomain

## Phase 1: Validation Mode

```bash
# Validate which subdomains in the list are alive
sudo ksubdomain verify -d subdomains.txt -o alive.txt

# Control bandwidth
sudo ksubdomain verify -d subdomains.txt -b 5m -o alive.txt

# Validate results from subfinder
subfinder -d target.com -o subs.txt
sudo ksubdomain verify -d subs.txt --silent -o verified.txt
```

## Phase 2: Enumeration Mode

```bash
# Enumerate subdomains
sudo ksubdomain enum -d target.com -o results.txt

# Use a custom wordlist
sudo ksubdomain enum -d target.com -f wordlist.txt -o results.txt

# Control bandwidth and retries
sudo ksubdomain enum -d target.com -b 10m --retry 3 -o results.txt
```

## Phase 3: Advanced Options

```bash
# Custom DNS resolvers
sudo ksubdomain verify -d subs.txt -r resolvers.txt

# Silent output
sudo ksubdomain verify -d subs.txt --silent

# High bandwidth (internal network environment)
sudo ksubdomain enum -d target.com -b 1g -o results.txt
```
