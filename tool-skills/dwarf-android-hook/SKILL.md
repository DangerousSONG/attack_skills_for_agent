---
name: dwarf-android-hook
description: 渗透工具 skill:Dwarf 的安装、参数速查与攻击场景 playbook。当任务涉及 移动平台攻击 需要调用 Dwarf 时使用。
when-to-use: 渗透工具 skill:Dwarf 的安装、参数速查与攻击场景 playbook。当任务涉及 移动平台攻击 需要调用 Dwarf 时使用。
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
