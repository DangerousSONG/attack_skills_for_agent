---
name: thefatrat-backdoor
description: "TheFatRat bundles evasion trojans into normal APK/EXE programs. Signals: payload development, weaponization, select number to generate"
zh-signals: "TheFatRat: 免杀木马捆绑正常程序(APK/EXE)。信号:载荷开发,武器化,选取编号生成。"
when-to-use: "Use when weaponizing payloads by bundling a trojan into a normal APK or EXE for social engineering delivery. Requires an interactive menu selection and a target platform."
---

# TheFatRat

- Attack Category: C07 Payload Development and Weaponization
- Upstream Repository: https://github.com/Screetsec/TheFatRat
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/Screetsec/TheFatRat && cd TheFatRat && chmod +x setup.sh && ./setup.sh
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./fatrat` | Menu-driven payload type selection |
| `backdooring apk` | Implant the payload into a normal APK |
| ` Powershell AV-evasion generation` | Select the number to generate |
| `fudwin` | Windows FUD option |

## Attack Scenario Playbook

### Bundle an AV-evading trojan into a normal program (APK/EXE)

```bash
./fatrat # choose Android → backdoor the original APK → generate a legitimate-looking app with meterpreter
```

## Notes

Integrates msfvenom with custom AV evasion; the output is still detected by mainstream AV/PlayProtect, so production use needs further refinement.
