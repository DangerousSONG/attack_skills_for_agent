---
name: nbtscan-netbios
description: 渗透工具 skill:nbtscan 的安装、参数速查与攻击场景 playbook。当任务涉及 内网发现与枚举 需要调用 nbtscan 时使用。
---

# nbtscan

- 攻击大类:C29 内网发现与枚举
- 上游仓库:https://github.com/scallywag/nbtscan
- 上游 License:LGPL-2.1(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install nbtscan
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `nbtscan 10.0.0.0/24` | NetBIOS 名称扫描 |
| `-r` | 使用 137 端口递归 |
| `-v` | 详细 |

## 攻击场景 Playbook

### 内网主机名快速普查

```bash
nbtscan -r 10.0.0.0/24
# 出主机名/域/MAC,比 ping 扫信息量大,找 DC/文件服务器快
```

## 注意事项

老牌 NetBIOS 枚举;内网第一天第一跑,主机名直接暴露角色。
