---
name: aquatone-visual-recon
description: "Aquatone: performs domain flyover visual verification. Signals: asset mapping, subdomain, aquatone, output directory, scan timeout"
zh-signals: "Aquatone: 域名飞越式可视化核查。信号:资产测绘,子域名,aquatone`,输出目录,扫描超时。"
when-to-use: >-
  Use when you have a list of subdomains or hosts and want screenshot-based visual
  triage of live web assets, clustered by response similarity.
---

# Aquatone

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/michenriksen/aquatone
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/michenriksen/aquatone@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `cat hosts.txt | aquatone` | Batch screenshots via piped input |
| `-ports large` | Port set (xlarge/large/medium/small) |
| `-out ./aquatone` | Output directory |
| `-scan-timeout 90000` | Scan timeout |
| `-screenshot-timeout 30000` | Screenshot timeout |

## Attack Scenario Playbook

### Domain Flyover Visual Verification

```bash
cat subdomains.txt | aquatone -out report -ports large
# report/aquatone_report.html clusters by response similarity, making admin consoles easy to spot
```

## Notes

Clusters and groups by response body similarity, ideal for quickly triaging a large subdomain list; project maintenance has slowed but the functionality is stable.
