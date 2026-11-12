---
name: kiterunner-api-routes
description: "kiterunner brute-forces hidden API routes. Signals: asset mapping, subdomain, API route scanning, built-in dictionary, maximum connections."
zh-signals: "kiterunner: API 隐藏路由爆破。信号:资产测绘,子域名,API 路由扫描,内置字典,最大连接。"
when-to-use: >-
  Use when brute-forcing hidden API routes that directory scanners miss; scan a
  target with the built-in Assetnote route wordlists and tune connections and
  crawl depth.
---

# kiterunner

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/assetnote/kiterunner
- Upstream License: AGPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/assetnote/kiterunner/cmd/kr@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `kr scan https://api.target.com -w routes.kite` | API route scanning |
| `-A=apiroutes-210228` | Built-in dictionary |
| `-x 100` | Maximum connections |
| `-d 3` | Crawl depth |
| `kr scan targets.txt --depth 3 -A` | Batch |

## Attack Scenario Playbook

### Brute-forcing hidden API routes

```bash
kr scan https://api.target.com -w ~/kiterunner/routes.kite -x 100
# By Assetnote, route context aware, great at surfacing endpoints like /internal/v2/admin
```

## Notes

API route discovery is an order of magnitude more accurate than directory brute forcers; the dictionary is built from real API traffic.
