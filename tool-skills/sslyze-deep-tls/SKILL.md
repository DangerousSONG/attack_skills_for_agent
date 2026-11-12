---
name: sslyze-deep-tls
description: "sslyze performs compliance-grade TLS assessment. Signals: cryptographic attack, cryptographic cracking, TLS deep scan, compliance check, certificate chain details"
zh-signals: "sslyze: 合规级 TLS 评估。信号:密码学攻击,加密破解,TLS 深度扫描,合规检查,证书链详情。"
when-to-use: >-
  Use when performing a deep TLS assessment against a host, including protocol
  support, cipher suites, certificate chain details, and Mozilla compliance
  checks.
---

# sslyze

- Attack Category: C49 Cryptographic Attacks
- Upstream Repository: https://github.com/nabla-c0d3/sslyze
- Upstream License: AGPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install sslyze
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `sslyze t.com` | TLS deep scan |
| `sslyze --mozilla_config=intermediate t.com` | Compliance check |
| `sslyze --certinfo t.com` | Certificate chain details |
| `-j out.json` | JSON output |

## Attack Scenario Playbook

### Compliance-grade TLS assessment

```bash
sslyze --mozilla_config=modern t.com -j tls.json
# Compare against the Mozilla configuration baseline
```

## Notes

Python TLS scanning library with deep protocol detection plus compliance checks.
