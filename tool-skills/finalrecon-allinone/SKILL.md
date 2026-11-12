---
name: finalrecon-allinone
description: "FinalRecon generates a full OSINT report for a single target. Signals: asset mapping, subdomains, full reconnaissance, DNS only, subdomains only."
zh-signals: "FinalRecon: 单目标全量 OSINT 报告。信号:资产测绘,子域名,全量侦察,仅 DNS,仅子域。"
when-to-use: "Use FinalRecon when you need a one-shot reconnaissance report for a single target, covering DNS, WHOIS, subdomains, directories, ports, tech stack, certificates, and historical URLs in a modular Markdown output."
---

# FinalRecon

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/thewhiteh4t/FinalRecon
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/thewhiteh4t/FinalRecon && cd FinalRecon && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 finalrecon.py --full https://target.com` | Full reconnaissance |
| `--dns` | DNS only |
| `--sub` | Subdomains only |
| `--dir` | Directories only |
| `--wayback` | History only |
| `-o dir` | Output |

## Attack Scenario Playbook

### Full OSINT Report for a Single Target

```bash
python3 finalrecon.py --full https://target.com -o report
# DNS/WHOIS/subdomains/directories/ports/tech stack/certificates/history in one Markdown report
```

## Notes

Modular report-style reconnaissance; the output is ready to paste directly into a penetration testing report appendix.
