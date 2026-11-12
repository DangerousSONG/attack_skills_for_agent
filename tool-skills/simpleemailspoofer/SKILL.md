---
name: simpleemailspoofer
description: "SimpleEmailSpoofer: phishing email spoofing test. Signals: phishing, social engineering, specified SMTP, HTML mode."
zh-signals: "SimpleEmailSpoofer: 钓鱼邮件伪造测试。信号:钓鱼,社会工程,指定 SMTP,HTML 模式。"
when-to-use: "Use in phishing assessments to send spoofed emails and test whether SPF, DKIM, and DMARC protections can be bypassed."
---

# SimpleEmailSpoofer

- Attack Category: C08 Phishing and Social Engineering
- Upstream Repository: https://github.com/lunarca/SimpleEmailSpoofer
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/lunarca/SimpleEmailSpoofer && cd SimpleEmailSpoofer
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python SimpleEmailSpoofer.py -e attacker@evil.com -t victim@corp.com -s 'Urgent' -m body.txt -f ceo@corp.com` | Email spoofing |
| `-e from -t to -s subj -m msg -f spoof` | Parameters |
| `-S server` | Specify SMTP server |
| `-p` | HTML mode |

## Attack Scenario Playbook

### Phishing Email Spoofing Test

```bash
python SimpleEmailSpoofer.py -e x@evil.com -t finance@corp.com -s 'Invoice' -m mail.txt -f ceo@corp.com
# Tests SPF/DKIM/DMARC bypass for red team phishing assessment
```

## Notes

Minimal SMTP spoofing tool for phishing exercises; evaluates SPF/DMARC configuration.
