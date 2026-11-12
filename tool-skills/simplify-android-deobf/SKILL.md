---
name: simplify-android-deobf
description: "simplify: Android malicious and hardened sample deobfuscation. Signals: mobile, Android attack, Android deobfuscation, specified classes only, single-method timeout."
zh-signals: "simplify: Android 恶意/加固样本反混淆。信号:移动端,android攻击,Android 反混淆,仅处理指定类,单方法超时。"
when-to-use: >-
  Use when analyzing packed or obfuscated Android malware and you want constant propagation and
  dead-code removal to make the smali logic readable.
---

# simplify

- Attack Category: C43 Mobile Platform Attacks
- Upstream Repository: https://github.com/CalebFenton/simplify
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/CalebFenton/simplify && ./gradlew fatjar
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `java -jar simplify/build/libs/simplify.jar app.apk -o simple.apk` | Android deobfuscation |
| `--include-classes com/corp/**` | Process only the specified classes |
| `--max-execution-time 30` | Per-method timeout |
| `-it` | Output intermediate results |

## Attack Scenario Playbook

### Deobfuscate malicious or hardened Android samples

```bash
java -jar simplify.jar packed.apk -o clean.apk
# After constant propagation/dead-code elimination the logic reads far better in jadx
```

## Notes

Android dex deobfuscation and anti-VM-detection tool, well suited to analyzing packed or obfuscated samples.
