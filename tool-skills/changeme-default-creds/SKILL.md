---
name: changeme-default-creds
description: "changeme: Scans the internet for default credentials. Signals: port scanning, nmap, default credential scanning, specified application."
zh-signals: "changeme: 默认口令全网扫描。信号:端口扫描,nmap,默认凭据扫描,指定应用。"
when-to-use: >-
  Use during network-wide scanning when you want to test many hosts and
  applications for default credentials across common ports.
---

# changeme

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/ztgrace/changeme
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/ztgrace/changeme && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `changeme -s 10.0.0.0/24` | Default credential scanning |
| `-s subnet -p 22,80,443` | Ports |
| `-a tomcat,apache` | Specified applications |
| `-o out.json` | Output |

## Attack Scenario Playbook

### Internet-Wide Default Credential Scanning

```bash
changeme -s 10.0.0.0/24 -p 22,80,443,3306
# Default credentials on routers, cameras and databases
```

## Notes

A default credential scanner with a default password database covering 289+ applications.
