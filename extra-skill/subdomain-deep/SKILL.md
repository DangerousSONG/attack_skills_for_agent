---
name: subdomain-deep
description: "Deep subdomain mining with multi-source joint enumeration. Use when you need to maximize subdomain discovery coverage, regular DNS enumeration results are insufficient, or the target uses CDN/wildcard DNS. Combine DNS brute-forcing, OSINT engines, and crawlers for cross-source discovery"
zh-signals: "联合 DNS 爆破、OSINT 与爬虫多源交叉挖掘子域名，最大化资产覆盖率。信号:子域名,深度枚举,dns,osint,爬虫,资产发现"
when-to-use: >-
  Use when regular DNS enumeration is insufficient, or when the target uses CDN/wildcard DNS
  and you need maximum subdomain coverage across multiple independent sources.
metadata:
  tags: "recon,subdomain,dns,osint,crawl,subdomain-enumeration,bruteforce,DNS,asset-discovery,amass,subfinder"
  category: "recon"
---

# Deep Subdomain Mining Methodology

> **⛔ In-depth reference**: the full parameters of subfinder/ksubdomain/amass, wildcard filtering scripts, and the multi-tool combined workflow are in `references/enumeration-tools.md`

Single-source subdomain enumeration usually covers only 30-50% of the actual assets. This methodology combines three independent sources for cross-validation and maximizes coverage.

## Phase 1: DNS Enumeration
Use `subfinder` / `ksubdomain` for DNS subdomain enumeration (wordlist brute-forcing + recursive discovery).

**Result analysis**:
- Count subdomains resolving to different IP ranges (identify multi-datacenter / multi-cloud deployments)
- Identify CNAME records → CDN/cloud services (CloudFront, Cloudflare, Fastly)
- Identify wildcards: if `random12345.example.com` also resolves, wildcard records exist
  - When a wildcard exists, filter out results matching the wildcard IP

## Phase 2: OSINT Engine Searches
Query the FOFA API through `http_request` or `curl` to find assets associated with the domain. OSINT engines can discover assets missed by DNS enumeration (because they are based on real network scan data rather than DNS records).

**What OSINT can add**:
- Web services on non-standard ports (e.g. `dev.example.com:8443`)
- "Ghost" subdomains whose DNS records were deleted but whose services are still online
- Other domains on the same server, found by reverse IP lookup

## Phase 3: Crawler Discovery
Use `katana` to crawl the main site and known subdomains, extracting additional subdomain references from page content.

**Sources the crawler can find**:
- Links in HTML (href/src/action)
- Hardcoded API addresses in JavaScript
- Resource domains referenced in CSS
- Cross-origin request headers (CORS: Access-Control-Allow-Origin)

## Phase 4: Result Merging and Classification

After deduplicating and merging the subdomains from the three sources, classify them by purpose:

| Type | Characteristics | Attack value |
|------|------|----------|
| Web application | 80/443, HTTP response | High — primary attack surface |
| API service | api.*/gateway.* | High — often has authentication flaws |
| Admin panel | admin.*/manage.*/cms.* | Very high — direct administrative access |
| Mail system | mail.*/smtp.*/mx.* | Medium — phishing and information gathering |
| Development/testing | dev.*/test.*/staging.* | Very high — weakest security controls |
| Internal system | vpn.*/oa.*/git.*/jenkins.* | Very high — should not be reachable from the public internet |
| CDN/static | cdn.*/static.*/img.* | Low — usually no dynamic content |

**Priority for deeper probing**: admin panels > development/testing > internal systems > API > web applications

## Wildcard Handling
- Wildcard DNS detection: after wordlist enumeration, compare content — use HTTP response comparison to distinguish real subdomains from fakes

## CNAME/CDN Identification
- S3 bucket: points at `s3.amazonaws.com` via CNAME
- When 404/bucket not declared, it may be possible to register a same-named bucket and take it over
