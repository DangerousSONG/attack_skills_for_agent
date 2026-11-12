---
name: secretfinder-js-secrets
description: "SecretFinder: harvests hardcoded secrets from frontend JS. Signals: API attack, interface testing, JS secret extraction, bulk, simultaneous crawling."
zh-signals: "SecretFinder: 前端 JS 硬编码密钥收割。信号:api攻击,接口测试,JS 中秘密提取,批量,同时爬站。"
when-to-use: >-
  Use when analyzing frontend JavaScript files to extract hardcoded secrets such as
  AWS keys, Slack tokens, JWTs or private keys, individually or in bulk.
---

# SecretFinder

- Attack Category: C10 API and Business Logic Attacks
- Upstream Repository: https://github.com/mazen160/secrets-patterns-db
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/mazen160/secrets-patterns-db or the main SecretFinder repo
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python SecretFinder.py -i https://t.com/app.js -o results.txt` | Extract secrets from JS |
| `-i urls.txt` | Batch |
| `-e` | Crawl sites simultaneously |

## Attack Scenario Playbook

### Harvest Hardcoded Secrets from Frontend JS

```bash
python SecretFinder.py -i https://target/static/app.js -o keys.txt
# Regex matching across 40+ patterns: AWS keys, Slack tokens, JWTs, private keys
```

## Notes

A de facto tool for extracting frontend secrets; paired with linkfinder (endpoint discovery) it forms a complete JS analysis toolkit.
