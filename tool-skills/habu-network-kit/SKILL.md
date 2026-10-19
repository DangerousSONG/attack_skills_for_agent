---
name: habu-network-kit
description: 渗透工具 skill:habu 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 habu 时使用。
---

# habu

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/portantier/habu
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install habu
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `habu.ip -t t.com` | IP 信息 |
| `habu.arp -i eth0` | ARP 扫描 |
| `habu.tcpflags -t 10.0.0.5` | TCP 标志探测 |
| `habu.contest` | 连通性测试 |
| `habu.land -t ip` | LAND 攻击 |

## 攻击场景 Playbook

### 网络层 Swiss Army

```bash
habu.arp -i eth0 && habu.tcpflags -t 10.0.0.5
# ARP 发现+防火墙识别
```

## 注意事项

Python 网络工具集,100+ 命令,网络层渗透辅助。
