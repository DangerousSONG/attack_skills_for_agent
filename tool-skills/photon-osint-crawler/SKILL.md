---
name: photon-osint-crawler
description: "Full OSINT crawling. Signals: asset mapping, subdomains, full crawling, crawl depth, threads."
zh-signals: "Photon: OSINT 全量抓取。信号:资产测绘,子域名,全量爬取,爬深,线程。"
when-to-use: "Use Photon when performing OSINT asset mapping and you need to crawl a target site to archive URLs, emails, files, and API keys, with configurable crawl depth and threads."
---

# Photon

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/s0md3v/Photon
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/s0md3v/Photon && cd Photon && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python photon.py -u https://target.com` | Full crawl |
| `-l 3` | Crawl depth |
| `-t 10` | Threads |
| `-e json` | Export JSON |
| `--keys` | Extract API keys/tokens |
| `--dns` | DNS data |
| `-o dir` | Output directory |

## Attack Scenario Playbook

### Full OSINT Crawl

```bash
python photon.py -u https://target.com -l 3 --keys -e json
# Output: urls/emails/files/keys/intel stored in separate categories
```

## Notes

A crawler designed for OSINT that also picks up emails and keys along the way; --wayback can merge in historical data.
