---
name: barmie-rmi-attack
description: "BaRMIe: attacks Java RMI. Signals: lateral movement, psexec, RMI enumeration attack, attack modes, dictionary"
zh-signals: "BaRMIe: Java RMI 攻击。信号:横向移动,psexec,RMI 枚举攻击,攻击模式,字典。"
when-to-use: >-
  Use when targeting Java RMI services and you need to enumerate exposed
  objects and test them for insecure deserialization or known attack vectors.
---

# BaRMIe

- Attack Category: C31 Remote Service Lateral Movement
- Upstream Repository: https://github.com/NickstaDB/BaRMIe
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/NickstaDB/BaRMIe && cd BaRMIe
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `java -jar BaRMIe.jar -target 10.0.0.5 -port 1099` | RMI enumeration attack |
| `-attack` | Attack mode |
| `-wordlist w.txt` | Wordlist |

## Attack Scenario Playbook

### Java RMI Attack

```bash
java -jar BaRMIe.jar -target 10.0.0.5
# RMI enumeration + deserialization exploitation
```

## Notes

A Java RMI enumeration and attack tool that detects insecure deserialization.
