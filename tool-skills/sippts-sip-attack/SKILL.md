---
name: sippts-sip-attack
description: "sippts: internal VoIP attack. Signals: port scan, nmap, SIP scan, extension enumeration, SIP brute force."
zh-signals: "sippts: VoIP 内网攻击。信号:端口扫描,nmap,SIP 扫描,分机枚举,SIP 爆破。"
when-to-use: >-
  Use when attacking internal VoIP/SIP infrastructure and you need SIP scanning,
  extension enumeration, credential brute forcing or CallerID spoofing.
---

# sippts

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/Pepelux/sippts
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/Pepelux/sippts && cd sippts
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./sippts scan -i 10.0.0.0/24` | SIP scan |
| `extenum -i ip -e 100-999` | Extension enumeration |
| `crack -i ip -u 100 -w pass.txt` | SIP brute force |
| `spoof -i ip` | CallerID spoofing |

## Attack Scenario Playbook

### VoIP internal network attack

```bash
./sippts scan -i 10.0.0.0/24 && ./sippts extenum -i 10.0.0.5
# Discovery + enumeration + brute force
```

## Notes

A SIP toolset by Pepelux.