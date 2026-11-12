---
name: vulmap-vuln-scan
description: "Vulmap: Local CVE one-click scan. Signals: vulnerability intelligence, CVE, local vulnerability scan, update vulnerability database, specified application."
zh-signals: "Vulmap: 本地 CVE 一键扫。信号:漏洞情报,cve,本地漏洞扫描,更新漏洞库,指定应用。"
when-to-use: >-
  Use when you need to scan a local system and its middleware against a CVE
  database; supports updating the vulnerability database and limiting scanning
  to specified applications.
---

# Vulmap

- Attack Category: C06 Vulnerability Intelligence and Exploit Databases
- Upstream Repository: https://github.com/vulmon/Vulmap
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/vulmon/Vulmap && cd Vulmap/Unix && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 vulmap.py` | Local vulnerability scan |
| `-u` | Update the vulnerability database |
| `-a apache,nginx` | Specify applications |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### One-shot local CVE scan

```bash
python3 vulmap.py
# Matches system and middleware CVEs
```

## Notes

Local vulnerability scanner from Vulmon.
