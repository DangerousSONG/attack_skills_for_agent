---
name: striker-recon
description: "Striker rapidly profiles targets. Signals: web vulnerability, injection, reconnaissance and initial vulnerability triage, verbose"
zh-signals: "Striker: 目标快速画像。信号:web漏洞,注入,信息收集+漏洞初判,详细。"
when-to-use: "Use when you need rapid target profiling that combines information gathering with initial vulnerability triage covering WAF, cloud, CDN, subdomains, ports and common web flaws."
---

# Striker

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/UltimateHackers/Striker
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/UltimateHackers/Striker && cd Striker && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python striker.py t.com` | Information gathering + initial vulnerability triage |
| `-o report` | Output |
| `-d` | Verbose |

## Attack Scenario Playbook

### Rapid target profiling

```bash
python striker.py t.com
# WAF / cloud / CDN / subdomains / ports / common flaws in one shot
```

## Notes

Combines information gathering with initial vulnerability triage, outputting a target technology stack profile.
