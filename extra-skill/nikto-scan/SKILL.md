---
name: nikto-scan
description: "Scan web servers for vulnerabilities using Nikto. Use when you need to detect known web server vulnerabilities, outdated software versions, dangerous files/CGI, or misconfigurations. Nikto ships with 7000+ checks covering common OWASP issues. This skill applies to any web vulnerability scanning, server security assessment, or configuration audit scenario"
zh-signals: "使用 Nikto 扫描 Web 服务器已知漏洞、过时软件、危险文件与配置错误。信号:Nikto,Web扫描,漏洞扫描,CGI,配置错误"
when-to-use: >-
  Use when you need to scan a web server for known vulnerabilities, outdated software,
  dangerous files/CGI, or misconfigurations.
metadata:
  tags: "nikto,web,scan,vulnerability scanning,web server,CGI,misconfiguration,OWASP,SSL,outdated software"
  category: "tool"
---

# Nikto Web Server Vulnerability Scanning Methodology

Nikto is the classic web server vulnerability scanner. Core advantages: **rich check catalog** (7000+ checks) + **works out of the box** (no configuration) + **broad coverage** (outdated software / dangerous files / misconfigurations / known vulnerabilities).

Project address: https://github.com/sullo/nikto

## Phase 1: Basic Scanning

```bash
# Scan a single target
nikto -h http://target.com

# Specify a port
nikto -h target.com -p 8080

# HTTPS scan
nikto -h https://target.com

# Multi-port scan
nikto -h target.com -p 80,443,8080,8443
```

## Phase 2: Scan Tuning

```bash
# Specify the scan type (Tuning)
# 1=file upload 2=default file 3=information disclosure 4=injection 5=remote retrieval 6=DoS 7=remote shell 8=command execution 9=SQL injection
nikto -h http://target.com -Tuning 123489

# Run only the information disclosure checks
nikto -h http://target.com -Tuning 3

# Exclude the DoS checks
nikto -h http://target.com -Tuning x6

# Specify plugins
nikto -h http://target.com -Plugins apache_expect_xss,ssl

# Set the maximum scan time
nikto -h http://target.com -maxtime 300
```

## Phase 3: Authentication and Proxy

```bash
# Basic Auth
nikto -h http://target.com -id admin:password

# Cookie authentication
nikto -h http://target.com -Add-header "Cookie: session=abc123"

# Custom User-Agent
nikto -h http://target.com -useragent "Mozilla/5.0"

# Go through a proxy
nikto -h http://target.com -useproxy http://127.0.0.1:8080

# Disable 404 guessing (reduce false positives)
nikto -h http://target.com -no404
```

## Phase 4: Output Formats

```bash
# JSON output
nikto -h http://target.com -Format json -output results.json

# HTML report
nikto -h http://target.com -Format html -output report.html

# CSV output
nikto -h http://target.com -Format csv -output results.csv

# XML output
nikto -h http://target.com -Format xml -output results.xml
```

## Common Scenario Quick Reference

| Scenario | Command |
|------|------|
| Quick scan | `nikto -h http://target.com -maxtime 120` |
| Full scan | `nikto -h http://target.com -Tuning 123456789abc` |
| SSL check | `nikto -h https://target.com -Plugins ssl` |
| Information disclosure | `nikto -h http://target.com -Tuning 3` |
| Authenticated scan | `nikto -h http://target.com -id admin:pass` |
