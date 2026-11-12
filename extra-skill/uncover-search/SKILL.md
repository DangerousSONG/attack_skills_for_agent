---
name: uncover-search
description: "Use uncover to aggregate queries against internet search engines. Use when you need to rapidly discover exposed assets from engines such as Shodan/Censys/FOFA/Hunter/Quake/ZoomEye. uncover unifies the query interface of multiple search engines, so one command queries several engines. Any scenario involving asset discovery, internet-wide mapping, or exposure surface assessment should use this skill"
zh-signals: "使用 uncover 聚合 Shodan、Censys、FOFA、Hunter、Quake、ZoomEye 等引擎进行资产发现。信号:uncover,资产发现,互联网测绘,Shodan,FOFA,OSINT"
when-to-use: "Use when performing authorized asset discovery or internet-wide exposure mapping through multiple search engines via uncover."
metadata:
  tags: "uncover,search,shodan,censys,fofa,hunter,quake,zoomeye,asset-discovery,internet-mapping,OSINT"
  category: "tool"
---

# uncover Internet Search Engine Aggregation Methodology

uncover is a search engine aggregation tool from ProjectDiscovery. Core advantages: **unified multi-engine interface** (Shodan/Censys/FOFA/Hunter/Quake/ZoomEye/Netlas) + **one command, multiple sources** + **pipeline friendly**.

Project URL: https://github.com/projectdiscovery/uncover

API key configuration: edit `~/.config/uncover/provider-config.yaml` to add the API key for each engine.

## Phase 1: Basic Search

```bash
# Shodan search
uncover -q "org:target.com" -e shodan

# FOFA search
uncover -q 'domain="target.com"' -e fofa

# Censys search
uncover -q "target.com" -e censys

# query multiple engines at once
uncover -q "target.com" -e shodan,censys,fofa
```

## Phase 2: Advanced Search

```bash
# limit the number of results
uncover -q "apache" -e shodan -l 200

# JSON output
uncover -q "org:target.com" -e shodan -json -o results.json

# silent output (only shows IP:Port)
uncover -q "org:target.com" -e shodan -silent

# read queries from a file
uncover -ql queries.txt -e shodan
```

## Phase 3: Pipeline Integration

```bash
# asset discovery → HTTP liveness check
uncover -q "org:target.com" -e shodan -silent | httpx -silent

# asset discovery → port scanning
uncover -q "org:target.com" -e shodan -silent | naabu -silent

# asset discovery → vulnerability scanning
uncover -q 'domain="target.com"' -e fofa -silent | httpx -silent | nuclei
```

## Query Syntax per Engine

| Engine | Domain Query | Organization Query |
|------|---------|---------|
| Shodan | `hostname:target.com` | `org:"Target Inc"` |
| Censys | `target.com` | `autonomous_system.name:"Target"` |
| FOFA | `domain="target.com"` | `org="Target Inc"` |
| Hunter | `domain="target.com"` | `icp.name="Target"` |
| Quake | `domain:"target.com"` | `org:"Target Inc"` |
