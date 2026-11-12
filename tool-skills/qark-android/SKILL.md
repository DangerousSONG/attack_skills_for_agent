---
name: qark-android
description: "QARK: Static APK vulnerability scanner. Signals: mobile, Android attack, APK static scanning, JSON report, generate executable PoC."
zh-signals: "QARK: APK 静态漏洞扫描。信号:移动端,android攻击,APK 静态扫描,JSON 报告,生成可执行 PoC。"
when-to-use: >-
  Use when statically scanning an Android APK for exported components, weak
  crypto, hardcoded secrets, and WebView issues; generate a JSON report and
  optional proof-of-concept exploits.
---

# QARK

- Attack Category: C43 Mobile Attacks
- Upstream Repository: https://github.com/linkedin/qark
- Upstream License: NOASSERTION (manual review required) (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install qark
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `qark --apk app.apk` | APK static scan |
| `--report-type json` | JSON report |
| `--exploit-apk` | Generate an executable PoC |
| `-o outdir` | Output |

## Attack Scenario Playbook

### Static APK vulnerability scanning

```bash
qark --apk target.apk --report-type json
# Detects: exported components/weak crypto/hardcoded secrets/WebView configuration/SDK vulnerabilities
```

## Notes

By LinkedIn; the report contains vulnerability details and remediation recommendations, making it suitable for quick assessment.
