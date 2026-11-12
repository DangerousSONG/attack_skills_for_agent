---
name: raccoon-offensive-recon
description: "Raccoon: One-stop single-target reconnaissance. Signals: asset mapping, subdomains, one-stop reconnaissance, output directory, via Tor."
zh-signals: "Raccoon: 单目标一站式摸底。信号:资产测绘,子域名,一站式侦察,输出目录,走 Tor。"
when-to-use: "Use when you need one-stop reconnaissance of a single target covering subdomains, ports, and fingerprints in a structured output directory. Requires a target domain and optionally Tor routing."
---

# Raccoon

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/evyatarmeged/Raccoon
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install raccoon-scanner
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `raccoon target.com` | One-stop reconnaissance |
| `-o out` | Output directory |
| `--tor` | Route via Tor |
| `-f` | Force all modules |
| `--dns` | DNS only |
| `--subdomains` | Subdomains only |

## Attack Scenario Playbook

### One-Stop Reconnaissance of a Single Target

```bash
raccoon corp.com -o raccoon_out
# DNS/WHOIS/subdomains/ports/fingerprints/Nmap all run in one pass
```

## Notes

Aggregated reconnaissance with a clear output directory structure; the Nmap integration means the report already carries port conclusions.
