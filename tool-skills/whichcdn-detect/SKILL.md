---
name: whichcdn-detect
description: "whichCDN: CDN identification for bypass strategy selection. Signals: web vulnerabilities, injection, batch."
zh-signals: "whichCDN: CDN 识别选绕过策略。信号:web漏洞,注入,批量。"
when-to-use: "Use whichCDN when you need to identify whether a target sits behind a CDN and which provider it uses, including batch host lists, to choose an appropriate bypass strategy."
---

# whichCDN

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/Nitr4x/whichCDN
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/Nitr4x/whichCDN && cd whichCDN && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python whichCDN.py https://t.com` | CDN identification |
| `-i hosts.txt` | Batch |

## Attack Scenario Playbook

### CDN Identification to Select a Bypass Strategy

```bash
python whichCDN.py https://t.com
# Targeted bypass against Cloudflare/Akamai/Incapsula
```

## Notes

A CDN identification tool with fingerprints for 18+ providers.
