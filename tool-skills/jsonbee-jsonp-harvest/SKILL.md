---
name: jsonbee-jsonp-harvest
description: "JSONBee hijacks JSONP callbacks. Signals: payload development, weaponization, usable JSONP endpoints, XSS or data theft, curated endpoints."
zh-signals: "JSONBee: JSONP 回调劫持。信号:载荷开发,武器化,挑可用 JSONP 端点,XSS/数据窃取,预整理端点。"
when-to-use: >-
  Use when developing or weaponizing XSS and data-theft payloads that need a working JSONP endpoint with a controllable callback to leak cross-origin data.
---

# JSONBee

- Attack Category: C07 Payload and File Delivery
- Upstream Repository: https://github.com/zigoo0/JSONBee
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/zigoo0/JSONBee
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `grep -h 'google' *.txt` | Pick usable JSONP endpoints |
| `Combined payload: <script src='https://victim.com/jsonp?callback=steal'></script>` | XSS / data theft |
| `cc-ideal.jsonp file, view in bulk` | Curated endpoints |

## Attack Scenario Playbook

### JSONP Callback Hijacking

```bash
cat cc-ideal.jsonp | head
# Find JSONP endpoints holding sensitive data and forge the callback function to steal it
```

## Notes

A collection of JSONP endpoints (google/github/default callbacks, etc.), a resource library for XSS and cross-origin data theft.
