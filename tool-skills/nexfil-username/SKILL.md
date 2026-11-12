---
name: nexfil-username
description: "nexfil: Cross-platform username tracking. Signals: email collection, employee information, username internet-wide existence, concurrency."
zh-signals: "nexfil: 用户名跨平台追踪。信号:邮箱收集,员工信息,用户名全网存在性,并发。"
when-to-use: >-
  Use when you have a username or email and need to enumerate which social and
  web platforms the target has registered on for OSINT or employee profiling.
---

# nexfil

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/thewhiteh4t/nexfil
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/thewhiteh4t/nexfil && cd nexfil && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 nexfil.py -u username` | Internet-wide username existence check |
| `-u user -c 50` | Concurrency |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Cross-Platform Username Tracking

```bash
python3 nexfil.py -u targetuser
# Existence across 350+ platforms
```

## Notes

By whiteh4t, a username OSINT tool.
