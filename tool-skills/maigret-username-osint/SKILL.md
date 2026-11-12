---
name: maigret-username-osint
description: "Maigret: Full-web username profiling and targeted verification. Signals: email collection, employee information, 6000+ sites username lookup, full mode slow but complete."
zh-signals: "Maigret: 用户名全网画像、定向核验。信号:邮箱收集,员工信息,6000+ 站点查用户名,全量模式(慢但全)。"
when-to-use: "Use Maigret when you need to profile a username across thousands of sites or verify a person's social, code, and forum accounts during people OSINT, including gathering associated emails and employee information."
---

# Maigret

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/soxoj/maigret
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install maigret
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `maigret username` | Username lookup across 6000+ sites |
| `-a` | Full mode (slow but complete) |
| `-n 20` | Number of concurrent sites |
| `--pdf` | PDF report |
| `--json simple` | JSON output |
| `-c --site GitHub` | Only check the specified sites |

## Attack Scenario Playbook

### Full-web username profiling

```bash
maigret johndoe2024 --pdf
# Aggregates every public profile of that username across social networks, code sites, and forums
```

### Targeted verification

```bash
maigret suspect -c --site github --site twitter --site telegram
```

## Notes

An enhanced fork of Sherlock with a 6000+ site database; the PDF/HTML report is directly deliverable.
