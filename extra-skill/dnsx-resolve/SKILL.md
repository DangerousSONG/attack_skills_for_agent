---
name: dnsx-resolve
description: "Use dnsx for bulk DNS record querying and resolution. Use when you need bulk DNS resolution, subdomain liveness validation, A/AAAA/CNAME/NS/MX/TXT record queries, or wildcard filtering. dnsx is a high-speed DNS toolkit from ProjectDiscovery, supporting multiple record type queries and automatic wildcard filtering. Any scenario involving DNS resolution, subdomain validation, or DNS record collection should use this skill"
zh-signals: "使用 dnsx 进行批量 DNS 记录查询、子域名验证和通配符过滤。信号:DNS解析,子域名验证,dnsx,记录查询,通配符过滤"
when-to-use: >-
  Use when bulk-resolving DNS records, validating subdomain liveness, or filtering wildcard domains with ProjectDiscovery tooling.
metadata:
  tags: "dnsx,dns,resolve,dns-resolution,subdomain-validation,A-record,CNAME,MX,TXT,wildcard,projectdiscovery"
  category: "tool"
---

# dnsx Bulk DNS Resolution Methodology

dnsx is a high-speed DNS tool from ProjectDiscovery. Core advantages: **multiple record types** + **automatic wildcard filtering** + **pipeline friendly**.

Project URL: https://github.com/projectdiscovery/dnsx

## Phase 1: Basic Resolution

```bash
# A record for a single domain
echo target.com | dnsx -a -resp

# bulk resolution
dnsx -l subdomains.txt -a -resp -silent

# multiple record types
echo target.com | dnsx -a -aaaa -cname -ns -mx -txt -resp
```

## Phase 2: Subdomain Validation

```bash
# validate subdomain liveness
subfinder -d target.com -silent | dnsx -silent

# filter out wildcard domains
subfinder -d target.com -silent | dnsx -wd target.com -silent

# extract IP addresses
subfinder -d target.com -silent | dnsx -a -resp-only -silent | sort -u
```

## Phase 3: Advanced Usage

```bash
# brute-force enumerate subdomains
dnsx -d target.com -w subdomains-wordlist.txt -silent

# custom DNS resolvers
dnsx -l domains.txt -a -resp -r 8.8.8.8,1.1.1.1

# PTR reverse resolution
echo 10.0.0.1 | dnsx -ptr -resp

# JSON output
dnsx -l domains.txt -a -resp -json -o results.json

# Control concurrency
dnsx -l domains.txt -a -t 200 -silent
```

## Pipeline Integration

```bash
# subdomain → DNS resolution → IP deduplication
subfinder -d target.com -silent | dnsx -a -resp-only -silent | sort -u

# subdomain → DNS validation → HTTP liveness check
subfinder -d target.com -silent | dnsx -silent | httpx -silent

# CNAME extraction (for subdomain takeover detection)
subfinder -d target.com -silent | dnsx -cname -resp -silent
```
