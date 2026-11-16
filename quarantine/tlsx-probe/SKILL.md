---
name: tlsx-probe
description: "Use tlsx for TLS certificate and configuration analysis. Use it when you need to extract SSL/TLS certificate details (SAN/CN), detect TLS versions, cipher suites, JARM/JA3 fingerprints, or certificate misconfigurations. tlsx is a TLS probing tool by ProjectDiscovery. Use this skill for any SSL/TLS analysis, certificate information gathering, or JARM fingerprinting scenario."
zh-signals: "使用 tlsx 提取 TLS 证书与配置信息，检测 TLS 版本、加密套件与 JARM/JA3 指纹。信号:tlsx,TLS证书,JARM,加密套件,证书分析"
when-to-use: >-
  Use when you need to extract SSL/TLS certificate details, probe TLS versions and cipher suites,
  or fingerprint JARM/JA3 on authorized targets.
metadata:
  tags: "tlsx,tls,ssl,certificate,SAN,CN,JARM,JA3,cipher-suite,projectdiscovery"
  category: "tool"
---

# tlsx TLS Certificate Analysis Methodology

tlsx is a TLS probing tool by ProjectDiscovery. Core strengths: **certificate information extraction** + **JARM/JA3 fingerprinting** + **misconfiguration detection** + **pipeline friendly**.

Project URL: https://github.com/projectdiscovery/tlsx

## Phase 1: Basic Probing

```bash
# Single target
echo target.com | tlsx

# Extract certificate information
echo target.com | tlsx -san -cn -so -silent

# TLS versions and cipher suites
echo target.com | tlsx -tv -cipher -silent

# JARM fingerprint
echo target.com | tlsx -jarm -silent
```

## Phase 2: Certificate Analysis

```bash
# Full certificate information
echo target.com | tlsx -san -cn -so -tv -cipher -jarm -json

# Certificate expiry detection
echo target.com | tlsx -ex -silent

# Self-signed certificate detection
echo target.com | tlsx -ss -silent

# Domain mismatch detection
echo target.com | tlsx -mm -silent

# Batch check for certificate issues
tlsx -l hosts.txt -ex -ss -mm -re -un -silent
```

## Phase 3: Pipeline Integration

```bash
# Subdomains -> TLS certificate collection
subfinder -d target.com -silent | tlsx -san -cn -resp-only -silent

# Port scan -> TLS probing
naabu -host target.com -p 443,8443 -silent | tlsx -san -cn -silent

# Discover more subdomains from TLS SANs
echo target.com | tlsx -san -resp-only -silent | sort -u

# JSON output
tlsx -l hosts.txt -san -cn -tv -jarm -json -o results.json
```
