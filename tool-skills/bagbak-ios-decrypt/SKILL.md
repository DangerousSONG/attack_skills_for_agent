---
name: bagbak-ios-decrypt
description: "bagbak: extracts and unpacks App Store apps. Signals: mobile, android attack, export and decrypt specified app, list device apps, overwrite installed packages"
zh-signals: "bagbak: App Store 应用脱壳提取。信号:移动端,android攻击,导出并解密指定 App,列出设备 App,覆盖已安装包。"
when-to-use: >-
  Use on a jailbroken iOS device when you need to list installed apps and
  export or decrypt App Store IPAs for reverse engineering.
---

# bagbak

- Attack Category: C43 Mobile Platform Attacks
- Upstream Repository: https://github.com/ChiChou/bagbak
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
npm install -g bagbak
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `bagbak com.tencent.xin` | Export and decrypt a specified app |
| `bagbak -l` | List device apps |
| `bagbak -f com.app` | Overwrite the installed package |
| `-o out/` | Output directory |

## Attack Scenario Playbook

### App Store app decryption and extraction

```bash
bagbak -l  # Find the bundle id
bagbak com.corp.app  # Decrypt the IPA and write it to disk
```

## Notes

One-click export and decryption of IPAs on jailbroken iOS (FairPlay DRM unpacking), the first step of reverse engineering an app.
