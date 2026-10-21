---
name: powershdll-nopowershell
description: 渗透工具 skill:PowerShdll 的安装、参数速查与攻击场景 playbook。当任务涉及 Windows本地提权 需要调用 PowerShdll 时使用。
when-to-use: 渗透工具 skill:PowerShdll 的安装、参数速查与攻击场景 playbook。当任务涉及 Windows本地提权 需要调用 PowerShdll 时使用。
---

# PowerShdll

- 攻击大类:C17 Windows本地提权
- 上游仓库:https://github.com/p3nt4/PowerShdll
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/p3nt4/PowerShdll && cd dll 目录用 rundll32 直接调
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `rundll32 PowerShdll.dll,main -s <script.ps1>` | 无 powershell.exe 执行脚本 |
| `rundll32 PowerShdll.dll,main -c <cmdlet>` | 单条命令 |
| `regsvr32 /s PowerShdll.dll` | 注册表模式 |
| `InstallUtil 模式绕过 AppLocker` | 说明 |

## 攻击场景 Playbook

### Constrained Language 模式绕过

```bash
rundll32 PowerShdll.dll,main -s enum.ps1
# powershell.exe 被禁/CLM 锁定时经 rundll32 跑 PowerShell
```

## 注意事项

通过 rundll32/regsvr32 宿主跑 PowerShell,绕过 powershell.exe 禁用、AppLocker、CLM 限制。
