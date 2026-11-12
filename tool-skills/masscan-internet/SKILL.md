---
name: masscan-internet
description: "masscan: Network-wide fast mapping and banner-level service identification. Signals: port scanning, nmap, full subnet full port high-speed scan, banner fingerprinting."
zh-signals: "masscan: 网段级快速测绘、Banner 级服务识别。信号:端口扫描,nmap,全网段全端口高速扫,带 banner 抓指纹。"
when-to-use: "Use when you need internet-scale or full-subnet high-speed port scanning with banner grabbing for service identification. Requires root privileges, target ranges, and rate and interface settings to avoid flooding."
---

# masscan

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/robertdavidgraham/masscan
- Upstream License: AGPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install masscan or build from source
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `masscan 10.0.0.0/8 -p0-65535 --rate 100000` | Full subnet, full port high-speed scan |
| `-p445,3389,22 --banner` | Grab banners for fingerprinting |
| `--excludefile exclude.txt` | Exclusion list |
| `-oG out.gnmap` | Grepable output |
| `--rate` | Packet send rate (pps) |

## Attack Scenario Playbook

### Network segment level fast mapping

```bash
masscan 172.16.0.0/12 -p1-65535 --rate 30000 -oG mass.gnmap
# After the results: awk '{print $4}' mass.gnmap | cut -d/ -f1 | sort -u > alive.txt
```

### Banner level service identification

```bash
masscan 10.0.0.0/24 -p443 --banners --rate 5000
```

## Notes

Asynchronous SYN scanning, and the rate can be pushed to 100k pps or more; note that an excessive rate can take down low-end network gear, so try a low rate first in an authorized environment.
