---
name: netdiscover-arp
description: Netdiscover: 二层存活发现(绕过禁 ping)。信号:内网枚举,网络发现,ARP 存活扫描,指定网卡,被动模式。
---

# Netdiscover

- 攻击大类:C29 内网发现与枚举
- 上游仓库:https://github.com/netdiscover-scanner/netdiscover
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install netdiscover
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `netdiscover -r 10.0.0.0/24` | ARP 存活扫描 |
| `-i eth0` | 指定网卡 |
| `-p` | 被动模式 |
| `-c 3` | 发包次数 |

## 攻击场景 Playbook

### 二层存活发现(绕过禁 ping)

```bash
netdiscover -r 10.0.0.0/16 -i eth0
# ARP 层探测,目标防火墙/ICMP 全封也逃不掉
```

## 注意事项

ARP 发现是内网最底层可靠的存活手段;被动模式(-p)零发包。
