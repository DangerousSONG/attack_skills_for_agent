---
name: cloudfail-cloud-origin
description: "CloudFail: Locates origin IPs behind CDNs. Signals: red team, methodology, bypassing Cloudflare to find origin IP, scanning all subdomains, Tor exit nodes to avoid blocking."
zh-signals: "CloudFail: CDN 后源站 IP 定位。信号:红队,方法论,绕过 CF 找源站 IP,扫描全部子域,Tor 出口防封。"
when-to-use: >-
  Use when a target is protected by Cloudflare or another CDN and you need to
  locate the real origin IP via historical DNS records and non-CDN subdomains,
  optionally routing through Tor to avoid blocking.
---

# CloudFail

- Attack Category: C50 Trace Cleanup and Anti-Forensics
- Upstream Repository: https://github.com/m0rtem/CloudFail
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/m0rtem/CloudFail && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 cloudfail.py --target t.com` | Bypass Cloudflare to find the origin IP |
| `-s` | Scan all subdomains |
| `--tor` | Use Tor exit nodes to avoid blocking |

## Attack Scenario Playbook

### Locating origin IPs behind a CDN

```bash
python3 cloudfail.py --target t.com --tor
# Historical DNS records plus subdomain side channels yield the origin, letting you bypass the WAF directly
```

## Notes

Uses historical DNS data and non-CDN subdomains to locate the real origin behind Cloudflare.
