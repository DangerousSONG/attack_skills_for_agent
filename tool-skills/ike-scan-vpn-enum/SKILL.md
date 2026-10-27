---
name: ike-scan-vpn-enum
description: ike-scan: VPN 网关探测+PSK 破解。信号:端口扫描,nmap,IKE 服务发现+指纹,多行输出(易读)。
---

# ike-scan

- 攻击大类:C42 网络服务枚举
- 上游仓库:https://github.com/royhills/ike-scan
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install ike-scan
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `ike-scan 10.0.0.1` | IKE 服务发现+指纹 |
| `-M` | 多行输出(易读) |
| `-A` |  aggressive 模式组名枚举 |
| `-P` | PSK 抓取(hashcat -m 5400 破) |
| `-n payload.txt` | 自定义 transform |

## 攻击场景 Playbook

### VPN 网关探测+PSK 破解

```bash
ike-scan -M -A 10.0.0.1
# 出 IKE 指纹+AGGRESSIVE 模式握手哈希,hashcat -m 5400 破 PSK
```

## 注意事项

IPsec/IKE VPN 探测标准工具,aggressive 模式抓 PSK 哈希离线破解。
