---
name: xray-recon-map
description: "XRay: Shodan data-driven asset graph. Signals: asset mapping, subdomains, Shodan-driven mapping, dictionary mode."
zh-signals: "XRay: Shodan 数据驱动的资产图谱。信号:资产测绘,子域名,Shodan 驱动测绘,字典模式。"
when-to-use: >-
  Use when mapping an authorized domain's assets through Shodan data instead of active
  scanning, optionally with a wordlist, to produce a service and vulnerability graph.
---

# XRay

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/evilsocket/xray
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/evilsocket/xray@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `xray -shodan-key X -domain corp.com` | Shodan-driven mapping |
| `-domain corp.com -wordlist words.txt` | Wordlist mode |

## Attack Scenario Playbook

### Shodan Data-Driven Asset Graph

```bash
xray -shodan-key $KEY -domain corp.com -o report
# automatic: Shodan search of the target → port/service/vulnerability correlation → HTML graph
```

## Notes

From evilsocket; uses Shodan data instead of active scanning, which is extremely stealthy.
