---
name: apachetomcatscanner-tomcat
description: "ApacheTomcatScanner: maps Tomcat services network-wide. Signals: port scan, nmap, Tomcat scan, weak credentials"
zh-signals: "ApacheTomcatScanner: Tomcat 全网测绘。信号:端口扫描,nmap,Tomcat 扫描,弱口令。"
when-to-use: >-
  Use during network-wide scanning to identify Tomcat services, versions, default
  paths, and weak credentials.
---

# ApacheTomcatScanner

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/p0dalirius/ApacheTomcatScanner
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install apachetomcatscanner
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `apachetomcatscanner -t 10.0.0.0/24` | Tomcat scan |
| `-t cidr -u admin -p pass` | Weak credentials |
| `-o out.txt` | Output |
| `--list-modules` | Module list |

## Attack Scenario Playbook

### Network-wide Tomcat mapping

```bash
apachetomcatscanner -t 10.0.0.0/24
# Version / default paths / weak credentials / CVEs
```

## Notes

By p0dalirius; a dedicated Tomcat scanner.
