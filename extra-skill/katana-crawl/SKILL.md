---
name: katana-crawl
description: "Web crawling and URL discovery with katana. Use when you need to crawl all pages and endpoints of a target site, discover hidden API paths, endpoints inside JavaScript, or extract forms. katana is the next-generation crawler framework from ProjectDiscovery, supporting both standard mode and Headless browser mode, and able to parse JavaScript to discover dynamic endpoints. Any scenario involving web crawling, URL discovery, JS endpoint extraction, form discovery, or sitemap discovery should use this skill"
zh-signals: "使用 katana 进行 Web 爬虫与 URL/JS 端点发现。信号:katana,爬虫,URL发现,JS端点,headless"
when-to-use: "Use when crawling a target website for pages, endpoints, JS-referenced API paths, forms, or sitemap discovery with katana."
metadata:
  tags: "katana,crawl,spider,web crawler,URL discovery,JS parsing,endpoint,form,projectdiscovery,headless"
  category: "tool"
---

# katana Web Crawler Methodology

katana is the next-generation web crawler framework from ProjectDiscovery. Core advantages: **JavaScript parsing** (discovers dynamic endpoints) + **Headless mode** (renders SPAs) + **pipeline friendly** + **automatic form filling**.

Project address: https://github.com/projectdiscovery/katana

## Phase 1: Basic Crawling

```bash
# Crawl a single target (default depth 3)
katana -u http://target.com

# Specify crawl depth
katana -u http://target.com -d 5

# Silent output (URLs only)
katana -u http://target.com -silent

# Output to file
katana -u http://target.com -silent -o urls.txt
```

## Phase 2: JavaScript Parsing (Key Capability)

Modern web applications use JS frameworks heavily, and traditional crawlers cannot find API endpoints hardcoded in JS:

```bash
# Enable JS endpoint parsing (recommended to always enable)
katana -u http://target.com -jc

# Enable jsluice deep JS parsing (more thorough, higher memory usage)
katana -u http://target.com -jsluice

# Headless mode (crawl after rendering the page, suitable for SPA/React/Vue)
katana -u http://target.com -headless

# Headless + use system Chrome
katana -u http://target.com -headless -system-chrome
```

## Phase 3: Batch Crawling

```bash
# Read targets from a file
katana -list urls.txt -silent

# Pipe from stdin
cat urls.txt | katana -silent

# Combine with other tools
subfinder -d target.com -silent | httpx -silent | katana -silent -jc
```

## Phase 4: Output Filtering

```bash
# Only output specific extensions
katana -u http://target.com -em php,jsp,asp -silent

# Exclude static assets
katana -u http://target.com -ef png,jpg,css,gif,svg,woff -silent

# Regex match (only output URLs containing api)
katana -u http://target.com -mr "api|admin|login" -silent

# Regex filter (exclude URLs containing logout)
katana -u http://target.com -fr "logout|static" -silent

# Extract form elements
katana -u http://target.com -form-extraction -jsonl
```

## Phase 5: Scope Control

```bash
# Restrict to the same domain (default behavior)
katana -u http://target.com

# Show external endpoints (display only, not crawled)
katana -u http://target.com -display-out-scope

# Custom scope (regex)
katana -u http://target.com -crawl-scope "target\.com|api\.target\.com"

# Exclude specific paths
katana -u http://target.com -crawl-out-scope "logout|signout"

# No scope restriction (dangerous, use with care)
katana -u http://target.com -no-scope
```

## Phase 6: Advanced Configuration

```bash
# Time-limited crawl (important in CTF scenarios)
katana -u http://target.com -crawl-duration 60s

# Control concurrency and rate
katana -u http://target.com -c 20 -rl 100

# Custom Header (use a Cookie to access pages that require authentication)
katana -u http://target.com -H "Cookie: session=abc123"

# Use a proxy
katana -u http://target.com -proxy http://127.0.0.1:8080

# JSONL output (includes full request information)
katana -u http://target.com -jsonl -o results.jsonl

# Known file scan (robots.txt, sitemap.xml)
katana -u http://target.com -known-files all -d 3

# Technology detection
katana -u http://target.com -tech-detect

# XHR request extraction (Headless mode)
katana -u http://target.com -headless -xhr-extraction
```

## Phase 7: Pipeline Integration

```bash
# Crawler -> vulnerability scan
katana -u http://target.com -jc -silent | nuclei -severity critical,high

# Crawler -> filter JS files -> sensitive information extraction
katana -u http://target.com -jc -silent -em js | while read url; do
  curl -s "$url" | grep -iE "api_key|password|secret|token"
done

# Crawler -> parameter extraction -> SQLi testing
katana -u http://target.com -jc -silent | grep "?" | sort -u > params.txt

# Subdomain -> live hosts -> crawler -> vulnerability scan (full chain)
subfinder -d target.com -silent | httpx -silent | katana -jc -silent | nuclei
```

## Crawl Strategy Selection

| Scenario | Strategy | Command |
|------|------|------|
| Fast discovery (CTF) | Shallow crawl + JS | `katana -u URL -d 2 -jc -silent` |
| Full crawl | Deep crawl + Headless | `katana -u URL -d 5 -headless -jc` |
| API endpoint discovery | JS parsing + filtering | `katana -u URL -jc -em js,json -silent` |
| Post-authentication crawl | With Cookie | `katana -u URL -H "Cookie: ..." -jc` |
| SPA application | Headless is mandatory | `katana -u URL -headless -system-chrome` |
