---
name: appmon-ios-android
description: "appmon: monitors mobile app behavior. Signals: mobile, android attack, hook script directory, packet capture/data output, string monitoring"
zh-signals: "appmon: 移动 App 行为监控。信号:移动端,android攻击,hook 脚本目录,抓包/数据输出,字符串监控。"
when-to-use: >-
  Use when you need runtime introspection of an Android or iOS app to monitor
  sensitive behavior such as SQLite, Keychain, files and network traffic.
---

# appmon

- Attack Category: C43 Mobile Platform Attacks
- Upstream Repository: https://github.com/dpnishant/appmon
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/dpnishant/appmon && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python appmon.py -p android -a com.corp.app` | Attach to an Android app for monitoring |
| `-s scripts/` | Hook script directory |
| `-o out/` | Packet capture/data output |
| `--string` | String monitoring |

## Attack Scenario Playbook

### Mobile app behavior monitoring

```bash
python appmon.py -p ios -a com.corp.app  # Capture SQLite/NSUserDefaults/Keychain/network
```

## Notes

Monitors sensitive app behavior at runtime (database/files/network/keys) and outputs a structured report.
