---
name: ja3-fingerprint
description: "JA3 identifies threats using TLS fingerprints. Signals: asset mapping, subdomain."
zh-signals: "JA3: TLS 指纹威胁识别。信号:资产测绘,子域名。"
when-to-use: >-
  Use when analyzing captured TLS traffic (pcap) to extract JA3 fingerprints
  and identify malware or C2 families even when the traffic is encrypted.
---

# JA3

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/salesforce/ja3
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/salesforce/ja3
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python ja3.py -r traffic.pcap` | Extract TLS fingerprints from a pcap |
| `ja3 fingerprint database comparison` | Identify malware/C2 families |

## Attack Scenario Playbook

### TLS Fingerprint Threat Identification

```bash
python ja3.py -r capture.pcap | jq '.ja3'
# Compare fingerprints against public databases to identify C2/malware families (even when encrypted)
```

## Notes

The Salesforce TLS fingerprinting standard; JA3S/JA4 share the same origin and form the basis of threat hunting on encrypted traffic.
