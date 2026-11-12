---
name: wafw00f-waf-detect
description: "WAFW00F: Probe WAF before attacking. Signals: asset mapping, subdomains, identify WAF, list identifiable products, full detection mode."
zh-signals: "WAFW00F: 打前先探 WAF。信号:资产测绘,子域名,识别 WAF,列出可识别产品,全量检测模式。"
when-to-use: >-
  Use when fingerprinting a web target before attacking to identify the WAF
  product and decide on bypass and rate-limiting strategy.
---

# WAFW00F

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/EnableSecurity/wafw00f
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install wafw00f
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `wafw00f target.com` | Identify WAF |
| `-l` | List identifiable products |
| `-a` | Full detection mode |
| `-v` | Verbose output |
| `--proxy` | Proxy |

## Attack Scenario Playbook

### Probe the WAF before attacking

```bash
wafw00f api.target.com
# Output like 'cloudflare'/'aliyun' → decides the bypass strategy and rate limit
```

## Notes

Identify the WAF first, then decide the approach; the detection result directly guides whatwaf/manual bypass selection.
