---
name: whatweb-fingerprint
description: "WhatWeb: Batch fingerprint batch scanning. Signals: asset mapping, subdomains, single target fingerprint, aggression level 1-4, JSON log."
zh-signals: "WhatWeb: 批量指纹批扫。信号:资产测绘,子域名,单目标指纹,侵略等级(1-4),JSON 日志。"
when-to-use: "Use for asset fingerprinting at scale, identifying web technologies, versions, and plugins on single or many targets."
---

# WhatWeb

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/urbanadventurer/WhatWeb
- Upstream License: LGPL-2.1 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install whatweb or git clone + bundle install
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `whatweb target.com` | Single target fingerprint |
| `-i hosts.txt` | Batch |
| `-a 3` | Aggression level (1-4) |
| `--log-json out.json` | JSON log |
| `-v` | Verbose |
| `--follow-redirect=never` | Do not follow redirects |

## Attack Scenario Playbook

### Batch Fingerprinting

```bash
whatweb -i ips.txt -t 50 --log-json=web.json
# Extract plugin hits from the JSON: jq -r '.plugins | keys[]' web.json
```

## Notes

A plugin-based fingerprint database with more than 1800 entries; aggression level 3 may trigger WAFs, so use it within the authorized scope.
