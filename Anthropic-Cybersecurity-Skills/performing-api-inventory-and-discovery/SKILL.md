---
name: performing-api-inventory-and-discovery
description: 'Performs API inventory and discovery to identify all API endpoints in
when-to-use: 'Performs API inventory and discovery to identify all API endpoints in
  an organization''s environment including documented, undocumented, shadow, zombie,
  and deprecated APIs. The tester uses passive traffic analysis, active scanning,
  DNS enumeration, JavaScript analysis, and cloud resource inventory to build a comprehensive
  API catalog. Maps to OWASP API9:2023 Improper Inventory Management. Activates for
  requests involving API discovery, shadow API detection, API inventory audit, or
  attack surface mapping.

  '
domain: cybersecurity
subdomain: api-security
tags:
- api-security
- owasp
- api-discovery
- shadow-api
- inventory
- attack-surface
version: 1.0.0
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
- T1552.001
- T1078.004
- T1530
---
# Performing API Inventory and Discovery

## When to Use

- Mapping the complete API attack surface of an organization before a security assessment
- Identifying shadow APIs deployed by development teams without security review
- Discovering deprecated or zombie API versions that remain accessible but unmaintained
- Finding undocumented API endpoints exposed through mobile applications, SPAs, or microservices
- Building an API inventory for compliance requirements (PCI-DSS, SOC2, GDPR)

**Do not use** without written authorization. API discovery involves scanning network infrastructure and analyzing traffic.

## Prerequisites

- Written authorization specifying the target domains and network ranges
- Passive traffic capture capability (network tap, proxy, or cloud traffic mirroring)
- Active scanning tools: Amass, subfinder, httpx, and nuclei
- JavaScript analysis tools: LinkFinder, JS-Miner, or custom parsers
- Access to cloud console (AWS, Azure, GCP) for API gateway inventory
- Burp Suite Professional for passive API endpoint discovery

## Workflow

### Step 1: Passive API Discovery from Traffic Analysis

```python
import re
import json
from collections import defaultdict

# Parse HAR file from browser developer tools or proxy
def analyze_har_for_apis(har_file_path):
    """Extract API endpoints from HTTP Archive (HAR) file."""
    with open(har_file_path) as f:
        har = json.load(f)

    api_endpoints = defaultdict(lambda: {
        "methods": set(), "content_types": set(),
        "auth_types": set(), "count": 0
    })

    for entry in har["log"]["entries"]:
        url = entry["request"]["url"]
        method = entry["request"]["method"]

        # Identify API patterns
        api_patterns = [
            r'/api/', r'/v\d+/', r'/graphql', r'/rest/',
            r'/ws/', r'/rpc/', r'/grpc', r'/json',
        ]

        if any(re.search(p, url) for p in api_patterns):
            # Normalize the URL (remove query params and IDs)
            normalized = re.sub(r'\?.*$', '', url)
            normalized = re.sub(r'/\d+(/|$)', '/{id}\\1', normalized)
            normalized = re.sub(
                r'/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
                '/{uuid}', normalized)

            ep = api_endpoints[normalized]
            ep["methods"].add(method)
            ep["count"] += 1

            # Detect authentication type
            for header in entry["request"]["headers"]:
                name = header["name"].lower()
                if name == "authorization":
                    if "bearer" in header["value"].lower():
                        ep["auth_types"].add("Bearer/JWT")
                    elif "basic" in header["value"].lower():
                        ep["auth_types"].add("Basic")
                elif name == "x-api-key":
                    ep["auth_types"].add("API Key")

            # Detect content type
            content_type = next(
                (h["value"] for h in entry["request"]["headers"]
                 if h["name"].lower() == "content-type"), None)
            if content_type:
                ep["content_types"].add(content_type.split(";")[0])

    print(f"Discovered {len(api_endpoints)} unique API endpoints:\n")
    for url, info in sorted(api_endpoints.items()):
        methods = ", ".join(sorted(info["methods"]))
        auth = ", ".join(info["auth_types"]) or "None"
        print(f"  [{methods}] {url}")
        print(f"    Auth: {auth} | Requests: {info['count']}")

    return api_endpoints
```

### Step 2: Active API Endpoint Discovery

```bash
# DNS enumeration for API subdomains
amass enum -d example.com -o amass_results.txt
subfinder -d example.com -o subfinder_results.txt

# Filter for API-related subdomains
grep -iE '(api|rest|graphql|ws|gateway|backend|internal|staging|dev|v1|v2)' \
    amass_results.txt subfinder_results.txt | sort -u > api_subdomains.txt

# Check which subdomains are alive
cat api_subdomains.txt | httpx -status-code -content-length -title \
    -tech-detect -o live_apis.txt

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
