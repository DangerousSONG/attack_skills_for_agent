---
name: httpx-probe
description: "Use httpx for HTTP liveness probing, fingerprinting, and information gathering. Use when you need to batch-detect live HTTP/HTTPS services, identify the web technology stack, extract page titles/status codes/response headers, detect CDNs, or capture screenshots. httpx is a multi-purpose HTTP probe tool by ProjectDiscovery and is the key bridge between port scanning and vulnerability scanning in a penetration testing pipeline. Use this skill for any scenario involving HTTP liveness detection, web fingerprinting, technology stack identification, or batch URL probing"
zh-signals: "使用 httpx 进行 HTTP 探活、指纹识别与技术栈信息收集，是渗透测试管道的探测桥梁。信号:httpx,HTTP探活,指纹识别,技术栈,CDN检测"
when-to-use: "Use when batch-detecting live HTTP/HTTPS services, identifying web technologies, extracting titles, status codes, headers, CDN info, or screenshots."
metadata:
  tags: "httpx,probe,http,fingerprint,liveness detection,fingerprinting,tech stack,CDN,screenshot,projectdiscovery,title"
  category: "tool"
---

# httpx HTTP Liveness Detection and Fingerprinting Methodology

httpx is a multi-purpose HTTP probe tool by ProjectDiscovery. Its core strengths: **high-speed concurrency** (50 threads by default) + **rich probes** (status code/title/tech stack/CDN/screenshot, etc.) + **pipeline core** (the bridge between port scanning and vulnerability scanning).

Project address: https://github.com/projectdiscovery/httpx

## Phase 1: Basic Liveness Detection

```bash
# Single target
httpx -u http://target.com

# Batch targets (from a file)
httpx -l urls.txt

# Pipe from stdin
cat urls.txt | httpx

# Quiet output (only live URLs)
cat urls.txt | httpx -silent
```

## Phase 2: Information Probes (Core Capabilities)

```bash
# Show status code + title + tech stack (most common combination)
httpx -l urls.txt -sc -title -tech-detect

# Show status code + content length + web server
httpx -l urls.txt -sc -cl -server

# Show IP + CNAME + ASN
httpx -l urls.txt -ip -cname -asn

# CDN/WAF detection
httpx -l urls.txt -cdn

# Response time
httpx -l urls.txt -rt

# Full information output
httpx -l urls.txt -sc -title -tech-detect -server -ip -cdn -cl
```

## Phase 3: Technology Stack Identification (Fingerprinting)

httpx ships with the Wappalyzer dataset and can identify web frameworks, CMS platforms, programming languages, etc.:

```bash
# Tech stack detection
httpx -u http://target.com -tech-detect

# Example output:
# http://target.com [200] [WordPress] [PHP,MySQL,Apache]

# Batch identification + JSON output
httpx -l urls.txt -tech-detect -json -o fingerprints.json

# Custom fingerprint file
httpx -l urls.txt -tech-detect -custom-fingerprint-file /path/to/fingerprints.json
```

## Phase 4: Filtering and Matching

```bash
# Only show targets returning 200 OK
httpx -l urls.txt -mc 200

# Exclude 404 and 403
httpx -l urls.txt -fc 404,403

# Match responses containing a specific string
httpx -l urls.txt -ms "admin"

# Regex matching
httpx -l urls.txt -mr "login|admin|dashboard"

# Filter by response length
httpx -l urls.txt -fl 0

# Match a specific CDN
httpx -l urls.txt -match-cdn cloudflare

# Filter out error pages
httpx -l urls.txt -filter-page-type error,parked
```

## Phase 5: Screenshots (Headless)

```bash
# Page screenshot
httpx -l urls.txt -screenshot

# Use the system Chrome
httpx -l urls.txt -screenshot -system-chrome

# Screenshot + tech stack + status code
httpx -l urls.txt -screenshot -tech-detect -sc -title
```

## Phase 6: Pipeline Integration

httpx is the **core hub** of the ProjectDiscovery toolchain:

```bash
# Subdomains → HTTP liveness
subfinder -d target.com -silent | httpx -silent

# Port scan → HTTP liveness → fingerprint
naabu -host target.com -silent | httpx -tech-detect -title -sc

# Subdomains → liveness → vulnerability scan
subfinder -d target.com -silent | httpx -silent | nuclei -severity critical,high

# Subdomains → liveness → crawling → vulnerability scan (full chain)
subfinder -d target.com -silent | httpx -silent | katana -jc -silent | nuclei

# Network segment scan → HTTP liveness → fingerprint → high-value target filtering
naabu -host 10.0.0.0/24 -p 80,443,8080 -silent | httpx -tech-detect -title -sc -silent
```

## Phase 7: Advanced Usage

```bash
# Probe multiple ports (multi-port HTTP detection on a single host)
echo target.com | httpx -ports 80,443,8080,8443

# Custom request methods
httpx -l urls.txt -x GET,POST

# Custom header
httpx -l urls.txt -H "Cookie: session=abc"

# Follow redirects
httpx -l urls.txt -follow-redirects

# Grab TLS information
httpx -l urls.txt -tls-grab

# Extract regex matches (e.g. extracting email addresses)
httpx -l urls.txt -extract-preset mail,ipv4

# Custom regex extraction
httpx -l urls.txt -extract-regex "api[_-]?key['\"]?\s*[:=]\s*['\"]?([a-zA-Z0-9]+)"

# JSON output (with complete information)
httpx -l urls.txt -json -o results.json

# Control concurrency and rate
httpx -l urls.txt -threads 100 -rate-limit 50

# Deduplicate (filter similar pages)
httpx -l urls.txt -filter-duplicates
```

## Common Scenario Quick Reference

| Scenario | Command |
|------|------|
| Quick liveness detection | `cat urls.txt \| httpx -silent` |
| Tech stack identification | `httpx -l urls.txt -tech-detect -sc -title` |
| Find admin panels | `httpx -l urls.txt -mr "admin\|login\|dashboard" -sc -title` |
| CDN identification | `httpx -l urls.txt -cdn -ip` |
| Batch screenshots | `httpx -l urls.txt -screenshot -system-chrome` |
| Extract subdomains | `httpx -l urls.txt -extract-fqdn -json` |
| Chain with naabu | `naabu -host target -silent \| httpx -tech-detect` |
