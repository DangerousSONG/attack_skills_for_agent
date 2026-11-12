---
name: dwarf-android-hook
description: "Dwarf: Android runtime analysis. Signals: mobile, Android attack, launch GUI/CLI, attach process, Java method hooking."
zh-signals: "Dwarf: Android 运行时分析。信号:移动端,android攻击,启动 GUI/CLI,附加进程,Java 方法 hook。"
when-to-use: >-
  Use when performing authorized runtime analysis of an Android app: attach to
  the process, hook Java or native methods, and trace calls to understand
  authentication or anti-tampering logic.
---

# Dwarf

- Attack Category: C43 Mobile Platform Attacks
- Upstream Repository: https://github.com/iGio90/Dwarf
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip3 install dwarf-debugger
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `dwarf` | Launch GUI/CLI |
| `attach com.corp.app` | Attach to the process |
| `hook Java com.corp.app.LoginActivity.check` | Java method hook |
| `hook native 0x1234` | Native hook |
| `trace java com.corp.app.**` | Call tracing |

## Attack Scenario Playbook

### Android Runtime Analysis

```bash
dwarf  # Pick a device and attach to the target app
hook Java crypto function dump key/plaintext
```

## Notes

A Frida-based Android/iOS debugger that combines Java/native hooking, memory search and anti-anti-debugging in one tool.
