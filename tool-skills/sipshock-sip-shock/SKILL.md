---
name: sipshock-sip-shock
description: "sipshock: SIP device Shellshock testing. Signals: port scan, nmap, Range."
zh-signals: "sipshock: SIP 设备 Shellshock。信号:端口扫描,nmap,Range。"
when-to-use: "Use when scanning SIP devices for the Shellshock vulnerability (CVE-2014-6271) via crafted SIP headers."
---

# sipshock

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/zaf/sipshock
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/zaf/sipshock@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `sipshock -t 10.0.0.5` | SIP Shellshock scan |
| `-t ip -r` | Range |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Shellshock on SIP Devices

```bash
sipshock -t 10.0.0.0/24
# CVE-2014-6271 SIP header injection
```

## Notes

Shellshock detection for the SIP protocol.
