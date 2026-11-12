---
name: favfreak-favicon-hash
description: "FavFreak: group assets by same framework. Signals: asset mapping, subdomain, threads."
zh-signals: "FavFreak: 同框架资产归并。信号:资产测绘,子域名,线程。"
when-to-use: "Use to cluster assets by favicon hash so hosts running the same framework or CMS are grouped together."
---

# FavFreak

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/devanshbatham/FavFreak
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/devanshbatham/FavFreak && cd FavFreak
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `cat urls.txt | python3 favfreak.py` | Favicon hash clustering |
| `-o out.txt` | Output |
| `-t 20` | Threads |

## Attack Scenario Playbook

### Grouping Assets by Shared Framework

```bash
cat subs.txt | httpx -silent | python3 favfreak.py
# murmurhash clustering, one-shot grouping of assets running the same CMS
```

## Notes

Favicon murmurhash clustering quickly identifies assets sharing the same framework (admin panels / same CMS sites).
