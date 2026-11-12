---
name: microburst-azure
description: "MicroBurst: Azure credential harvesting and privilege escalation. Signals: cloud privilege escalation, IAM privilege escalation, credential collection, execute commands on VM, tenant information enumeration."
zh-signals: "MicroBurst: Azure 凭据收割+权限提升。信号:云提权,iam提权,凭据收集,VM 上执行命令,租户信息枚举。"
when-to-use: >-
  Use during Azure cloud penetration testing when you have credentials or a
  foothold and need to harvest secrets from KeyVault or Automation Accounts,
  enumerate tenant information, or run commands on VMs.
---

# MicroBurst

- Attack Category: C18 Cloud and Container Privilege Escalation
- Upstream Repository: https://github.com/NetSPI/MicroBurst
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/NetSPI/MicroBurst && Import-Module ./MicroBurst.psm1
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `Invoke-AzCredentialHarvest` | Credential collection |
| `Get-AzPasswords` | Export KeyVault/Automation credentials |
| `Invoke-AzVMCommand` | Run commands on a VM |
| `Get-AzDomainInfo` | Tenant information enumeration |
| `Invoke-EnumerateAzureSubDomains` | Subdomain enumeration |
| `Import-Module ./MicroBurst.psm1 -Verbose` | See the upstream documentation |

## Attack Scenario Playbook

### Azure credential harvesting and privilege escalation

```bash
Import-Module ./MicroBurst.psm1
Get-AzPasswords  # pull all secrets from Automation Accounts/KeyVault
Invoke-AzVMCommand -Script 'whoami'  # execute on the VM using Runbook permissions
```

## Notes

An Azure penetration PowerShell collection from NetSPI; credential harvesting (Runbook/KeyVault) is its core value.
