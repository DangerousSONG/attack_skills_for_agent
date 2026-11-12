---
name: gitem-github-org
description: "Gitem bulk clones and audits organization repositories. Signals: asset mapping, subdomains, pull all organization repos, metadata only."
zh-signals: "Gitem: 组织仓库批量克隆审计。信号:资产测绘,子域名,拉组织全部 repos,只 metadata。"
when-to-use: >-
  Use when enumerating a GitHub organization's repositories, cloning them all or fetching metadata before running secret scanners such as trufflehog or gitleaks.
---

# Gitem

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/mswell/gitem
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install gitem
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `gitem -u target` | Pull all organization repos |
| `-a` | Include releases/packages |
| `-m` | Metadata only |

## Attack Scenario Playbook

### Bulk clone and audit of organization repositories

```bash
gitem -u targetorg  # Clone all repos locally, then scan them in bulk for secrets with trufflehog/gitleaks
```

## Notes

Serves as the preparation step for organization-wide code auditing with secret scanners.
