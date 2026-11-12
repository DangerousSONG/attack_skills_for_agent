---
name: tlsx-tls-enum
description: "tlsx mines subdomains from certificate SANs. Signals: data collection, packaging, tlsx -cn -j, detailed enumeration, detect TLS misconfiguration"
zh-signals: "tlsx: 证书 SAN 挖子域。信号:数据收集,打包,tlsx -cn -j`,详细枚举,检测 TLS 配置错误。"
when-to-use: >-
  Use when gathering TLS and certificate intelligence, including extracting SAN/CN
  subdomains from IP ranges and detecting TLS misconfigurations.
---

# tlsx

- Attack Category: C33 URL and Content Discovery
- Upstream Repository: https://github.com/projectdiscovery/tlsx
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/projectdiscovery/tlsx/cmd/tlsx@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `tlsx -u t.com:443` | TLS version/cipher suites/certificate details |
| `cat ips.txt | tlsx -cn -j` | Batch extract certificate CN/SAN from IPs |
| `-san` | Output SAN domains (subdomain discovery) |
| `-ve` | Detailed enumeration |
| `-misconf` | Detect TLS misconfigurations |

## Attack Scenario Playbook

### Mining Subdomains from Certificate SANs

```bash
cat cidrs.txt | tlsx -san -j | jq -r '.san[]?' | sort -u
# Extract associated domains from certificates of every TLS service in the range
```

## Notes

By ProjectDiscovery, bulk extraction of TLS fingerprints + certificate data; a supplementary data source alongside amass/subfinder.
