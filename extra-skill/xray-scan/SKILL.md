---
name: xray-scan
description: "Automated web vulnerability scanning with xray. Use when a comprehensive vulnerability scan of a web application is required (XSS/SQLi/command injection/SSRF/XXE/path traversal/file upload/weak credentials, etc.). xray is a comprehensive web security assessment tool by Chaitin Tech that supports active scanning, passive proxy scanning, and basic crawler scanning, with rich built-in detection plugins and community POCs. Any scenario involving xray vulnerability scanning, web security assessment, or passive proxy scanning should use this skill"
zh-signals: "使用 xray 对 Web 应用进行主动、爬虫或被动代理漏洞扫描。信号:xray,漏洞扫描,Web安全,被动代理,POC,长亭"
when-to-use: "Use when performing automated web vulnerability scanning (XSS/SQLi/SSRF/XXE/etc.) with xray, including passive proxy and crawler modes."
metadata:
  tags: "xray,scan,web,vuln,vulnerability-scan,security-assessment,passive-scan,proxy-scan,chaitin,poc"
  category: "tool"
---

# xray Web Vulnerability Scanning Methodology

xray is a comprehensive web security assessment tool by Chaitin Tech. Its core strengths: **high detection accuracy** (semantic analysis engine) + **low false positive rate** + **rich community POC library**. It supports active scanning, passive proxy scanning, and crawler scanning.

Project URL: https://github.com/chaitin/xray

## Phase 1: Single URL Scan (Most Common)

```bash
# Scan a single URL (all plugins)
xray webscan --url http://target/?id=1 --html-output result.html

# Specify detection plugins (saves time)
xray webscan --url http://target/?id=1 --plugins sqldet,cmd-injection --html-output result.html

# JSON output (easy to parse)
xray webscan --url http://target/?id=1 --json-output result.json
```

## Phase 2: Crawler Scan (Automatic Page Discovery)

```bash
# Basic crawler + vulnerability scan
xray webscan --basic-crawler http://target --html-output crawl-result.html

# Specify crawler depth and plugins
xray webscan --basic-crawler http://target --plugins xss,sqldet,cmd-injection --html-output result.html
```

## Phase 3: Passive Proxy Scan

Suits manual testing with a browser; xray automatically analyzes traffic that passes through the proxy:

```bash
# Start the proxy listener
xray webscan --listen 127.0.0.1:7777 --html-output proxy-result.html

# Then set the browser/tool proxy to 127.0.0.1:7777
# All requests passing through the proxy are scanned automatically
```

## Phase 4: Detection Plugin Quick Reference

| Plugin key | What it detects | Notes |
|----------|---------|------|
| `xss` | XSS vulnerabilities | semantic analysis engine |
| `sqldet` | SQL injection | error-based/boolean-based/time-based blind injection |
| `cmd-injection` | command injection/code execution/SSTI | multiple payloads |
| `dirscan` | directory enumeration | backup files, config files, debug pages |
| `path-traversal` | path traversal | multi-platform, multi-encoding |
| `xxe` | XML entity injection | out-of-band + callback detection |
| `upload` | file upload | common backend languages |
| `brute-force` | weak credentials | HTTP basic auth + form based |
| `jsonp` | JSONP hijacking | cross-domain read of sensitive information |
| `ssrf` | SSRF | common bypasses + callback detection |
| `baseline` | baseline checks | SSL version, HTTP header checks |
| `redirect` | open redirect | meta/30x redirects |
| `crlf-injection` | CRLF injection | HTTP header injection |
| `struts` | Struts2 vulnerabilities | s2-016/032/045/059/061 (pro version)|
| `shiro` | Shiro deserialization | key detection (pro version)|
| `fastjson` | Fastjson vulnerabilities | series detection (pro version)|
| `thinkphp` | ThinkPHP vulnerabilities | series detection (pro version)|

### Plugin Combinations by Scenario

```bash
# Quick scan (high severity first, 1-2 minutes)
xray webscan --url URL --plugins sqldet,cmd-injection,xxe,ssrf

# Full scan (all plugins, default behavior)
xray webscan --url URL

# Web application testing (focused on web vulnerabilities)
xray webscan --url URL --plugins xss,sqldet,cmd-injection,upload,path-traversal

# Java applications (targeted)
xray webscan --url URL --plugins struts,shiro,fastjson,sqldet
```

## Phase 5: POC Scanning

xray has a built-in POC engine (phantasm) that supports community-contributed POCs:

```bash
# Scan with built-in POCs
xray webscan --plugins phantasm --url http://target

# Specify a custom POC directory
xray webscan --plugins phantasm --poc /path/to/pocs/ --url http://target
```

Community POC repository: https://github.com/chaitin/xray-plugins

## Configuration Tuning

```bash
# Generate a default configuration file
xray genca    # generate a CA certificate (required for the HTTPS proxy)

# Configuration file location: ~/.xray/config.yaml
# Common configuration items:
# - http.proxy: set an upstream proxy
# - http.headers: custom request headers
# - plugins.xxx.enabled: enable/disable a plugin
```

## Decision Table: xray vs nuclei

| Scenario | Recommended tool | Rationale |
|------|---------|------|
| Known CVE verification | **nuclei** | more complete template library (9000+) |
| General web vulnerability scanning | **xray** | semantic analysis, lower false positive rate |
| Passive proxy scanning | **xray** | native proxy mode support |
| Bulk target PoC detection | **nuclei** | better bulk performance |
| Deep SQL injection detection | **xray** | the sqldet engine is more accurate |
