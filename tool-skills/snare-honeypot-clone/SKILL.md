---
name: snare-honeypot-clone
description: "SNARE: clones target sites for phishing. Signals: web vulnerability, injection, start honeypot, clone site, Tanner verdict integration."
zh-signals: "SNARE: 克隆目标站钓鱼。信号:web漏洞,注入,起蜜罐,克隆站点,联动 Tanner 判定。"
when-to-use: >-
  Use when building a phishing or honeypot clone of a target site to capture
  credentials and observe attacker behavior, optionally integrating Tanner verdicts.
---

# SNARE

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/mushorg/snare
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install snare
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `snare --port 8080 --host-ip 0.0.0.0` | Start the honeypot |
| `snare --clone https://t.com` | Clone the site |
| `--tanner tanner.mushmush.org` | Integrate Tanner verdicts |

## Attack Scenario Playbook

### Clone the Target Site for Phishing

```bash
snare --clone https://login.t.com --port 443
# Mirror the login page + record credentials, works with DNS hijacking
```

## Notes

A honeypot / site cloning tool that faithfully reproduces any site.
