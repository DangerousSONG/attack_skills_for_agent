---
name: tls-prober-scan
description: "tls-prober fingerprints TLS stacks. Signals: asset mapping, subdomain, TLS implementation fingerprint, CSV output"
zh-signals: "tls-prober: TLS 栈指纹识别。信号:资产测绘,子域名,TLS 实现指纹,CSV 输出。"
when-to-use: >-
  Use when fingerprinting TLS implementations across a list of targets to
  narrow down library versions and CVE scope. Supports port selection and CSV
  output.
---

# tls-prober

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/x42/tls-prober
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/x42/tls-prober
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python prober.py -p 443,8443 targets.txt` | TLS implementation fingerprint |
| `-o out.csv` | CSV output |

## Attack Scenario Playbook

### TLS Stack Fingerprinting

```bash
python prober.py targets.txt  # Identify OpenSSL/GnuTLS/IIS versions to narrow the CVE scope
```

## Notes

Probes TLS libraries via the ClientHello fingerprint; often complements nmap service identification.
