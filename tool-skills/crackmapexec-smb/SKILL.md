---
name: crackmapexec-smb
description: "CrackMapExec / CME: Provides fast domain information over CIDR ranges. Signals: AD attack, domain penetration, SMB protocol alive enumeration, list SMB shares, remote hash extraction."
zh-signals: "CrackMapExec / CME: CIDR 级域内信息速览。信号:ad攻击,域渗透,SMB 协议枚举存活,列 SMB 共享,远程抓取哈希。"
---

# CrackMapExec / CME

- 攻击大类:C30 AD域渗透与域控攻击
- 上游仓库:https://github.com/byt3bl33d3r/CrackMapExec
- 上游 License:BSD-2-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install crackmapexec (项目已归档,生产建议用 NetExec)
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `crackmapexec smb 10.0.0.0/24` | SMB 协议枚举存活 |
| `-u user -p pass --shares` | 列 SMB 共享 |
| `--sam / --lsa / --ntds` | 远程抓取哈希 |
| `-M mimikatz` | 模块执行 |
| `--local-auth` | 本地认证绕过域策略 |

## 攻击场景 Playbook

### CIDR 级域内信息速览

```bash
crackmapexec smb 10.0.0.0/24 -u svc -p Pass123
# 输出主机名/域/签名状态/OS 一览表
```

## 注意事项

已归档但仍在大量环境预装;新环境用 NetExec 替代,语法几乎一致。本 skill 用于存量环境兼容。
