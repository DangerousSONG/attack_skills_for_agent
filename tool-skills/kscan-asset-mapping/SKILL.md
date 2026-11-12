---
name: kscan-asset-mapping
description: "Kscan unifies internal and external asset mapping. Signals: asset mapping, subdomain, subnet live hosts and fingerprints, weak password detection."
zh-signals: "Kscan: 内网+外网统一测绘。信号:资产测绘,子域名,网段存活+指纹,弱口令检测。"
when-to-use: >-
  Use for unified internal and external asset mapping: resolve subdomains,
  fingerprint live hosts across subnets, and detect weak passwords.
---

# Kscan

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/lcvvvv/kscan
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
Download the kscan binary from the release page
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `kscan -t target.com` | Asset mapping |
| `--spy` | Subnet live hosts + fingerprints |
| `-t 10.0.0.0/16` | Network segment |
| `--check` | Weak password detection |
| `--hydra` | Brute force integration |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Unified internal and external mapping

```bash
kscan --spy -o netmap.txt
kscan -t 10.0.0.0/16 --check  # live hosts / ports / fingerprints / weak passwords in one pass
```

## Notes
An all-in-one domestic mapping tool with built-in fingerprinting and weak password detection; the output is friendly for network segment surveying.
