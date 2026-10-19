---
name: seatbelt-host-survey
description: 渗透工具 skill:Seatbelt 的安装、参数速查与攻击场景 playbook。当任务涉及 Windows本地提权 需要调用 Seatbelt 时使用。
---

# Seatbelt

- 攻击大类:C17 Windows本地提权
- 上游仓库:https://github.com/GhostPack/Seatbelt
- 上游 License:BSD-3-Clause(GhostPack)(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
release 下载 Seatbelt.exe 或 dotnet build
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `Seatbelt.exe` | 全量主机侦察 |
| `Seatbelt.exe -group=user` | 按组 |
| `-group=system` | 系统组 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### Windows 提权面系统枚举

```bash
Seatbelt.exe -group=user -group=system
# 输出: 浏览器凭据/未引号服务路径/可写服务/AlwaysInstallElevated/UAC 配置
```

## 注意事项

GhostPack 出品 90+ 检查项;提权线索一网打尽,输出直接指导 privesc 路径。
