---
name: nextnet-as400
description: "nextnet: ICS/legacy system discovery. Signals: port scanning, nmap, special protocol discovery, AS400 scanning."
zh-signals: "nextnet: 工控/遗留系统发现。信号:端口扫描,nmap,特殊协议发现,AS400 扫描。"
when-to-use: >-
  Use when mapping ICS or legacy networks and you need to discover non-standard protocol devices
  such as AS/400 systems across a subnet.
---

# nextnet

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/hdm/nextnet
- Upstream License: BSD-2-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/hdm/nextnet@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `nextnet -p 1-10000 10.0.0.0/24` | Special protocol discovery |
| `-p ports -s as400` | AS400 scan |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### ICS/Legacy System Discovery

```bash
nextnet 10.0.0.0/16
# By hdm, discovers devices running non-standard protocols
```

## Notes

By hdm, a legacy system / ICS protocol discovery tool.
