---
name: spartan-sharepoint
description: "Spartan: asset mapping and fingerprinting. Signals: asset mapping, subdomain, deep enumeration."
zh-signals: "Spartan: 资产测绘与指纹识别场景。信号:资产测绘,子域名,深度枚举。"
when-to-use: "Use when targeting Microsoft SharePoint or FrontPage deployments to fingerprint the version, match historical CVEs, and probe sensitive paths. Requires the target URL and optionally deep enumeration."
---

# Spartan

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/NETSTAT-AFNL/Spartan
- Upstream License: NOASSERTION (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/NETSTAT-AFNL/Spartan
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python spartan.py -u https://t.com` | Frontpage/SharePoint fingerprint |
| `-e` | Deep enumeration |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### SharePoint/FrontPage Fingerprint + Vulnerability Matching

```bash
python spartan.py -u https://portal.corp.com
# Version identification → historical CVE matching → sensitive path probing (_vti_bin etc.)
```

## Notes

A SharePoint-focused scanner; old issues such as _vti_pvt/service.pwd are still worth picking up.
