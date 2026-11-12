---
name: gau-urlfetch
description: "Use gau to collect known URLs for a target domain from historical data sources. Use when you need to discover historical URLs, hidden endpoints, parameters, or API paths for a target. gau aggregates four data sources: Wayback Machine, Common Crawl, OTX and URLScan. Any scenario involving URL collection, attack surface discovery, parameter discovery, or historical page collection should use this skill"
zh-signals: "使用 gau 聚合 Wayback Machine、Common Crawl、OTX 与 URLScan 收集目标域名的历史 URL 和隐藏端点。信号:URL收集,历史URL,攻击面发现,参数发现,gau工具"
when-to-use: "Use when you need to discover historical URLs, hidden endpoints, parameters, or API paths for a target domain using passive data sources."
metadata:
  tags: "gau,url,fetch,url-collection,Wayback,historical-url,attack-surface,parameter-discovery,OSINT,information-gathering"
  category: "tool"
---

# gau URL History Collection Methodology

gau (getallurls) collects known URLs from historical data sources. Core advantages: **aggregation of four data sources** (Wayback/CommonCrawl/OTX/URLScan) + **fully passive** + **pipeline friendly**.

Project URL: https://github.com/lc/gau

## Phase 1: Basic Usage

```bash
# collect all known URLs for the target domain
gau target.com

# include subdomains
gau --subs target.com

# Output to file
gau target.com -o urls.txt

# filter out static assets
gau --blacklist png,jpg,gif,svg,woff,ttf,ico,css target.com
```

## Phase 2: Data Source Control

```bash
# specify data sources
gau --providers wayback target.com
gau --providers wayback,commoncrawl target.com

# time range
gau --from 202301 --to 202612 target.com

# control threads
gau --threads 10 target.com

# from stdin
echo target.com | gau
cat domains.txt | gau
```

## Phase 3: Pipeline Integration

```bash
# URL collection → extract URLs with parameters → XSS scan
gau target.com | grep "=" | sort -u | dalfox pipe --silence

# URL collection → extract JS files
gau target.com | grep "\.js$" | sort -u

# URL collection → extract API endpoints
gau target.com | grep -E "/api/|/v[0-9]/" | sort -u

# URL collection → liveness check
gau target.com | httpx -silent

# URL collection → sensitive paths
gau target.com | grep -iE "admin|backup|config|\.env|\.git|debug"
```

## Common Scenario Quick Reference

| Scenario | Command |
|------|------|
| Full collection | `gau --subs target.com -o all_urls.txt` |
| Parameterized URLs | `gau target.com \| grep "=" \| sort -u` |
| JS files | `gau target.com \| grep "\\.js$" \| sort -u` |
| API discovery | `gau target.com \| grep -E "/api/" \| sort -u` |
