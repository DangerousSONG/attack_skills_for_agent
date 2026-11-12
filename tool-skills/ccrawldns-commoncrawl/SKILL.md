---
name: ccrawldns-commoncrawl
description: "ccrawldns: Leverages CommonCrawl data sources. Signals: asset mapping, subdomains."
zh-signals: "ccrawldns: CommonCrawl 数据源利用。信号:资产测绘,子域名。"
when-to-use: >-
  Use when mining CommonCrawl for passive subdomains and URLs of a target
  domain; run it against the domain and combine with other passive sources such
  as gau or waybackurls.
---

# ccrawldns

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/ghostlulzhacks/ccrawldns
- Upstream License: NOASSERTION (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/ghostlulzhacks/ccrawldns
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python ccrawldns.py -t target.com` | Extract subdomains/URLs from CommonCrawl |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Leveraging CommonCrawl Data Sources

```bash
python ccrawldns.py -t corp.com
# free CommonCrawl index, includes new sites that Wayback does not have
```

## Notes

CommonCrawl is an often-overlooked passive data source; combine it with gau/waybackurls for three sources at once.
