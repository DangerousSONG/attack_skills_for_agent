---
name: apkleaks-endpoint-scan
description: "APKLeaks: checks mobile app API surface exposure. Signals: attack surface, cloud assets, scan APK endpoints/keys, custom rules, JSON output"
zh-signals: "APKLeaks: 移动应用 API 面暴露检查。信号:攻击面,云资产,扫 APK 端点/密钥,自定义规则,JSON 输出。"
when-to-use: >-
  Use when assessing the external attack surface of a mobile app; decompile an
  APK to extract hardcoded endpoints, URLs, and keys, optionally with custom
  rules and JSON output.
---

# APKLeaks

- Attack Category: C05 External Attack Surface and Cloud Asset Exposure
- Upstream Repository: https://github.com/dwisiswant0/apkleaks
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install apkleaks
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `apkleaks -f app.apk` | Scan APK endpoints and keys |
| `-p rules.json` | Custom rules |
| `-o out.json` | JSON output |
| `--json` | Force JSON output |

## Attack Scenario Playbook

### Mobile app API surface exposure check

```bash
apkleaks -f target-app.apk -o leaks.json
jq -r '.endpoints[]' leaks.json | sort -u  # Undisclosed APIs, test domains, and hardcoded keys
```

## Notes

Decompiles the APK to extract URLs, endpoints, and keys; on mobile targets this often hands you points for free.
