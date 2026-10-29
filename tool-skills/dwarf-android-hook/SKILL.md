---
name: dwarf-android-hook
description: "Dwarf: Android runtime analysis. Signals: mobile, Android attack, launch GUI/CLI, attach process, Java method hooking."
zh-signals: "Dwarf: Android 运行时分析。信号:移动端,android攻击,启动 GUI/CLI,附加进程,Java 方法 hook。"
---

# Dwarf

- 攻击大类:C43 移动平台攻击
- 上游仓库:https://github.com/iGio90/Dwarf
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip3 install dwarf-debugger
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `dwarf` | 启动 GUI/CLI |
| `attach com.corp.app` | 附加进程 |
| `hook Java com.corp.app.LoginActivity.check` | Java 方法 hook |
| `hook native 0x1234` | native hook |
| `trace java com.corp.app.**` | 调用跟踪 |

## 攻击场景 Playbook

### Android 运行时分析

```bash
dwarf  # 选设备附加目标 App
hook Java 加密函数 dump 密钥/明文
```

## 注意事项

基于 Frida 的 Android/iOS 调试器,Java/native hook+内存搜索+反反调试一体化。
