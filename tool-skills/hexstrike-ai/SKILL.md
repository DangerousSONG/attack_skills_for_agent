---
name: hexstrike-ai
description: "HexStrike-AI uses LLMs to assist penetration testing. Signals: AI security, LLM attack, AI-assisted pentest, modules, AI analysis."
zh-signals: "HexStrike-AI: LLM 辅助渗透测试。信号:ai安全,大模型攻击,AI 辅助渗透,模块,AI 分析。"
when-to-use: >-
  Use when you want an LLM-driven penetration testing assistant to plan and
  generate attack commands for a target. Requires the target URL or domain and
  optionally specifies a module or enables AI analysis.
---

# HexStrike-AI

- Attack Category: C44 AI and LLM Security
- Upstream Repository: https://github.com/0x4m4/hexstrike-ai
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/0x4m4/hexstrike-ai && cd hexstrike-ai && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 hexstrike.py -t 'https://t.com'` | AI-assisted pentest |
| `-t url -m nmap` | Module |
| `-t url -ai` | AI analysis |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### LLM-assisted penetration testing

```bash
python3 hexstrike.py -t corp.com
# Multi-agent AI pentest that generates commands automatically
```

## Notes

AI-driven penetration testing assistant.
