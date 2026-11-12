---
name: rmiscout-rmi-scan
description: "rmiscout: Finds unsafe Java RMI methods. Signals: lateral movement, psexec, RMI method brute forcing, fuzzing."
zh-signals: "rmiscout: Java RMI 不安全方法。信号:横向移动,psexec,RMI 方法爆破,fuzz。"
when-to-use: >-
  Use when enumerating exposed Java RMI registries to brute force method names and identify unsafe methods that can be abused for remote code execution or lateral movement.
---

# rmiscout

- Attack Category: C31 Remote Service Lateral Movement
- Upstream Repository: https://github.com/BishopFox/rmiscout
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/BishopFox/rmiscout && cd rmiscout && ./gradlew build
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `java -jar rmiscout.jar -i 10.0.0.5 -p 1099 wordlist.txt` | RMI method brute force |
| `-f` | fuzz |
| `-e` | Enumerate |

## Attack Scenario Playbook

### Unsafe Java RMI Methods

```bash
java -jar rmiscout.jar -i 10.0.0.5 -p 1099 /usr/share/wordlists/methods.txt
# Find abusable methods
```

## Notes

By BishopFox, an RMI method enumeration attack.
