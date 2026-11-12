---
name: smtptester-spoof
description: "SMTPTester: SPF and DKIM bypass testing. Signals: phishing, social engineering, SMTP spoof test, TLS."
zh-signals: "SMTPTester: SPF/DKIM 绕过测试。信号:钓鱼,社会工程,SMTP 伪造测试,TLS。"
when-to-use: "Use SMTPTester when testing whether a mail server can be abused to spoof sender addresses due to weak SPF/DKIM, e.g., during phishing and social-engineering assessment of a target's email infrastructure."
---

# SMTPTester

- Attack Category: C08 Phishing and Social Engineering
- Upstream Repository: https://github.com/xFreed0m/SMTPTester
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/xFreed0m/SMTPTester && cd SMTPTester && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 SMTPTester.py -t mail.t.com -f attacker@evil.com -v` | SMTP spoof test |
| `-t target -f from -to victim@corp.com` | Parameters |
| `-s` | TLS |

## Attack Scenario Playbook

### SPF/DKIM Bypass Test

```bash
python3 SMTPTester.py -t mail.t.com -f ceo@corp.com -to finance@corp.com
# Test email spoofing
```

## Notes

Tests SMTP open relays and spoofing.
