---
name: zgrab2-banner
description: "zgrab2: Internet-wide asset application-layer fingerprinting. Signals: asset mapping, subdomain, TLS certificate/fingerprint, SSH banner, JSON output."
zh-signals: "zgrab2: 全网资产应用层指纹。信号:资产测绘,子域名,TLS 证书/指纹,SSH banner,JSON 输出。"
when-to-use: >-
  Use when performing internet-wide or bulk application-layer fingerprinting from IP
  lists, capturing HTTP banners, TLS certificates/JA3 and SSH banners as JSON.
---

# zgrab2

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/zmap/zgrab2
- Upstream License: NOASSERTION (mainly Apache-2.0) (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/zmap/zgrab2@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `zgrab2 http -p 80,8080 < ips.txt` | HTTP banner capture |
| `zgrab2 tls -p 443` | TLS certificate/fingerprint |
| `zgrab2 ssh` | SSH banner |
| `-o out.json` | JSON output |

## Attack Scenario Playbook

### Internet-Wide Application-Layer Asset Fingerprinting

```bash
zmap -p 443 -o ips.txt 10.0.0.0/8
zgrab2 http tls -p 443,8443 -o banners.json < ips.txt
jq -r '.tls.server_certificates[0].parsed.subject.common_name[]?' banners.json | sort -u  # Extract certificate domain names
```

## Notes

The official application-layer companion to ZMap; grabs banners, certificates and JA3 hashes in bulk from an IP list.
