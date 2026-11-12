---
name: ntlmrecon-web-ntlm
description: "Discover NTLM authentication endpoints network-wide. Signals: AD attack, domain penetration, NTLM endpoint enumeration, subnet."
zh-signals: "ntlmrecon: NTLM 认证端点全网发现。信号:ad攻击,域渗透,NTLM 端点枚举,网段。"
when-to-use: >-
  Use during AD or web reconnaissance when you need to discover
  NTLM-authenticated endpoints such as Exchange, OWA, and Autodiscover and
  extract domain information across a subnet.
---

# ntlmrecon

- Attack Category: C30 AD Domain Penetration and Domain Controller Attacks
- Upstream Repository: https://github.com/sachinkamath/ntlmrecon
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install ntlmrecon
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `ntlmrecon -d t.com -i urls.txt` | NTLM endpoint enumeration |
| `-d domain -t 10.0.0.0/24` | Network segment |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Network-Wide Discovery of NTLM Authentication Endpoints

```bash
ntlmrecon -d t.com -i webpaths.txt
# Exchange/OWA/Autodiscover NTLM enumeration
```

## Notes

Web NTLM endpoint enumeration plus information extraction.
