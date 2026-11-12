---
name: sigploit-telecom
description: "SigPloit: SS7 and Diameter attacks. Signals: VPN vulnerability, firewall, telecom signaling attack framework, module."
zh-signals: "SigPloit: SS7/Diameter 攻击。信号:vpn漏洞,防火墙,电信信令攻击框架,模块。"
when-to-use: >-
  Use when testing SS7 or Diameter telecom signaling weaknesses in an
  authorized telecom environment; load the relevant module and set the target
  subscriber or network identifiers.
---

# SigPloit

- Attack Category: C11 Perimeter Device and VPN Attacks
- Upstream Repository: https://github.com/SigPloiter/SigPloit
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/SigPloiter/SigPloit
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python sigploit.py` | Telecom signaling attack framework |
| `use ss7/location_tracking` | Module |
| `set target +1234` | Target |

## Attack Scenario Playbook

### SS7/Diameter attacks

```bash
python sigploit.py && use ss7/intercept_sms
# Carrier signaling
```

## Notes

Telecom protocol attack framework.
