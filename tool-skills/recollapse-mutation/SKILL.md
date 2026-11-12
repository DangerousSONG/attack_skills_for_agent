---
name: recollapse-mutation
description: "recollapse: Generates 403-bypass parameter mutations. Signals: web vulnerabilities, injection, parameter mutation generation, value mutation, parameter name mutation."
zh-signals: "recollapse: 403 绕过参数变异。信号:web漏洞,注入,参数变异生成,值变异,参数名变异。"
when-to-use: >-
  Use when a web endpoint returns 403 and you need generated parameter value
  and parameter-name mutations to attempt a bypass.
---

# recollapse

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/0xacb/recollapse
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/0xacb/recollapse && cd recollapse && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 recollapse.py -u https://t.com/?id=1 -p id` | Parameter mutation generation |
| `-u url -mode values` | Value mutation |
| `-u url -mode names` | Parameter name mutation |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### 403 bypass parameter mutations

```bash
python3 recollapse.py -u https://t.com/admin -p path
# Generate encoding, case and duplicate parameter variants to bypass naive WAFs and routing restrictions
```

## Notes

Web parameter mutation tool that produces character-level and encoding-level variants, used to bypass filters and discover hidden endpoints.
