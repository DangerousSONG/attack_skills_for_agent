---
name: ntlm-challenger-check
description: "Extract NTLM information leakage. Signals: AD attack, domain penetration, parse NTLM authentication headers."
zh-signals: "ntlm-challenger: NTLM 信息泄露提取。信号:ad攻击,域渗透,解析 NTLM 认证头。"
when-to-use: "Use in AD reconnaissance to extract domain, host, and version information leaked via NTLM authentication headers."
---

# ntlm-challenger

- Attack Category: C30 AD Domain Penetration and Domain Controller Attacks
- Upstream Repository: https://github.com/b17zr/ntlm_challenger
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install ntlm-challenger
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `ntlm-challenger http://t.com/ntlm-auth` | Parse NTLM authentication headers |
| `-t url -o out.txt` | Output |

## Attack Scenario Playbook

### NTLM Information Leak Extraction

```bash
ntlm-challenger http://mail.t.com/autodiscover
# Extract domain, host and version to profile the internal network
```

## Notes

Parses HTTP NTLM challenge headers and leaks internal network information.
