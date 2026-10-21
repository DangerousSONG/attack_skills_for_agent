---
name: braa-snmp-mass
description: 渗透工具 skill:braa 的安装、参数速查与攻击场景 playbook。当任务涉及 网络服务枚举 需要调用 braa 时使用。
when-to-use: 渗透工具 skill:braa 的安装、参数速查与攻击场景 playbook。当任务涉及 网络服务枚举 需要调用 braa 时使用。
---

# braa

- 攻击大类:C42 网络服务枚举
- 上游仓库:https://github.com/mteg/braa
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install braa
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `braa public@10.0.0.0/24:.1.3.6.1.2.1.1.5` | 批量 SNMP 系统名查询 |
| `braa private@10.0.0.5:.1.3.6.1.4.1.77.1.2.25` | 用 private 团体串枚举用户 |
| `-t 1` | 超时/重试 |
| `public@x:.1.3.6.1.2.1.25.4.2.1.2` | 进程表 |

## 攻击场景 Playbook

### SNMP 团体串批量撞库

```bash
for c in public private community; do braa $c@10.0.0.0/24:.1.3.6.1.2.1.1.5; done
# 命中团体串→读系统信息/路由表/ARP 表
```

## 注意事项

SNMP 高速批量查询工具,一个进程扫全网段,配团体串字典效果极佳。
