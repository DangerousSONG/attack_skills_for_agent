---
name: passive-recon
description: "Purely passive OSINT intelligence collection that never touches the target. Use when you need to gather asset intelligence without the target noticing, for pre-engagement research before a formal penetration test, or to discover exposed assets through search engines such as FOFA/Quake/Hunter. Also applies to scenarios that require a complete asset view obtained by cross-comparing multiple engines"
zh-signals: "纯被动 OSINT 资产收集，使用 FOFA、Quake、Hunter 等引擎在不触碰目标的情况下发现暴露资产。信号:被动侦察,OSINT,FOFA,Quake,资产发现"
when-to-use: "Use when collecting target intelligence without touching the target, doing pre-engagement research, or cross-comparing search engines for asset discovery."
metadata:
  tags: "osint,passive,fofa,quake,hunter,passive reconnaissance,intelligence collection,asset discovery,search engine,whois,dns"
  category: "recon"
---

# Passive OSINT Intelligence Collection Methodology

> **⛔ In-depth reference**: the full query syntax and API invocation methods for each engine are in `references/search-engine-syntax.md`

The core advantage of passive reconnaissance is **zero contact** — it leaves no trace in the target's logs. It suits pre-engagement research, red team reconnaissance, or scenarios where only passive collection is allowed within the authorized scope.

## Phase 1: Multi-Engine Asset Search

### FOFA
Query the FOFA API (`https://fofa.info/api/v1/search/all?...`) via `http_request` or `curl` — the largest cyberspace mapping engine in China, ideal for discovering domestic assets.

Common query patterns:
- Domain assets: `domain="example.com"`
- IP range: `ip="192.168.1.0/24"`
- Specific service: `domain="example.com" && port="8080"`
- Specific component: `domain="example.com" && app="WordPress"`

### Quake
Query the Quake API (`https://quake.360.net/api/v3/search/quake_service`) via `http_request` or `curl` — 360's cyberspace mapping engine, strong at deep fingerprinting.

Common query patterns:
- Domain: `domain:"example.com"`
- Service: `domain:"example.com" AND port:8443`
- Component: `domain:"example.com" AND app:"Apache Tomcat"`

### Hunter
Query the Hunter API (`https://hunter.qianxin.com/openApi/search`) via `http_request` or `curl` — the Yingtu platform, strong at IP correlation analysis and asset aggregation.

## Phase 2: Cross-Comparison of Results

Each engine has its own emphasis, so only cross-comparison yields a complete view:

| Dimension | Analysis Method |
|------|----------|
| IP/domain inventory | Deduplicate and merge across the three engines, flagging those found by only one engine (possibly newly launched or decommissioned) |
| Port distribution | Count high-risk ports (22/3306/6379/9200), flagging non-standard ports |
| Technology stack | Aggregate web frameworks, middleware, and CMS versions |
| Admin panels | Search for assets whose title contains "login"/"admin"/"dashboard" |
| Certificate information | CN/SAN in SSL certificates may leak internal domain names |
| Historical data | Compare data across time points to discover newly added or decommissioned assets |

## Phase 3: High-Value Target Identification

Prioritize the following in the passively collected results:
1. **Exposed admin panels** — usually the shortest attack path
2. **Outdated/unmaintained services** — old component versions are more likely to have known vulnerabilities
3. **Internal systems exposed by mistake** — services such as OA/VPN/GitLab/Jenkins that should not be reachable from the public internet
4. **Exposed database ports** — unauthenticated Redis/MongoDB/Elasticsearch is a common problem
5. **Development/test environments** — dev/test/staging subdomains usually have weaker security controls

## Notes
- Purely passive collection, **do not** directly access or scan the target
- Search engine data has a time lag; the newest assets may not be indexed yet
- Query syntax differs between engines, so pay attention to the differences

## Multi-Engine Cross-Validation
- Results unique to a single engine may be newly launched or decommissioned
- Data timeliness: each engine indexes at a different time and updates at a different frequency
- Mark the source: flag assets found by only one engine, they require further verification
- Note: you may not scan, may not directly access the target, and may not port scan

## Other Passive Information Sources
- WHOIS domain registration lookups
- DNS history records
- GitHub searches for leaked code/credentials
- Other public sources (social media, forums, etc.)
