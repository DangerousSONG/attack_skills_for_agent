---
name: cero-tls-cert
description: "cero: Extracts subdomains from certificates in bulk. Signals: cryptographic attack, encryption cracking, bulk TLS certificate fetching, field selection."
zh-signals: "cero: 证书批量提取子域。信号:密码学攻击,加密破解,批量 TLS 证书抓取,字段选择。"
when-to-use: >-
  Use when you need to extract subdomains or certificate metadata in bulk by fetching TLS certificates across an IP range or CIDR for asset discovery.
---

# cero

- Attack Category: C49 Cryptographic Attacks
- Upstream Repository: https://github.com/glebarez/cero
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/glebarez/cero@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `cero 10.0.0.0/24 443` | Bulk TLS certificate fetching |
| `-o out.txt` | Output |
| `-s CN,SAN` | Field selection |

## Attack Scenario Playbook

### Bulk Subdomain Extraction from Certificates

```bash
cero 10.0.0.0/8 443 | tee certs.txt
# Extract CN/SAN from certificates across all TLS endpoints
```

## Notes

A Rust tool for bulk fetching TLS certificates and discovering subdomains within a range.
