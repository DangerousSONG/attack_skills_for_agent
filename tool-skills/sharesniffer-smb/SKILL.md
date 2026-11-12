---
name: sharesniffer-smb
description: "sharesniffer: batch internal network share discovery. Signals: internal enumeration, network discovery, SMB share sniffing."
zh-signals: "sharesniffer: 内网共享批量发现。信号:内网枚举,网络发现,SMB 共享嗅探。"
when-to-use: >-
  Use during internal enumeration to batch-discover accessible SMB shares across
  a subnet using anonymous or supplied credentials.
---

# sharesniffer

- Attack Category: C29 Internal Network Discovery and Enumeration
- Upstream Repository: https://github.com/shirosaidev/sharesniffer
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/shirosaidev/sharesniffer && cd sharesniffer
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 sharesniffer.py -h 10.0.0.0/24` | SMB share sniffing |
| `-h cidr -u user -p pass` | Credentials |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Batch Internal Network Share Discovery

```bash
python3 sharesniffer.py -h 10.0.0.0/24
# Dual mode: anonymous + authenticated
```

## Notes

SMB share discovery plus access testing.
