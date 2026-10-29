---
name: microburst-azure
description: "MicroBurst: Azure credential harvesting and privilege escalation. Signals: cloud privilege escalation, IAM privilege escalation, credential collection, execute commands on VM, tenant information enumeration."
zh-signals: "MicroBurst: Azure 凭据收割+权限提升。信号:云提权,iam提权,凭据收集,VM 上执行命令,租户信息枚举。"
---

# MicroBurst

- 攻击大类:C18 云与容器提权
- 上游仓库:https://github.com/NetSPI/MicroBurst
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/NetSPI/MicroBurst && Import-Module ./MicroBurst.psm1
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `Invoke-AzCredentialHarvest` | 凭据收集 |
| `Get-AzPasswords` | 导出 KeyVault/Automation 凭据 |
| `Invoke-AzVMCommand` | VM 上执行命令 |
| `Get-AzDomainInfo` | 租户信息枚举 |
| `Invoke-EnumerateAzureSubDomains` | 子域枚举 |
| `Import-Module ./MicroBurst.psm1 -Verbose` | 见上游文档 |

## 攻击场景 Playbook

### Azure 凭据收割+权限提升

```bash
Import-Module ./MicroBurst.psm1
Get-AzPasswords  # 拉 Automation Account/KeyVault 全部 secrets
Invoke-AzVMCommand -Script 'whoami'  # 用 Runbook 权限在 VM 执行
```

## 注意事项

NetSPI 出品的 Azure 渗透 PowerShell 集;凭据收割(Runbook/KeyVault)是核心价值。
