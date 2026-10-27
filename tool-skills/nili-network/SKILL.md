---
name: nili-network
description: nili: 扫描+MITM 一体。信号:端口扫描,nmap,网络扫描+中间人,嗅探,ARP 欺骗。
---

# nili

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/niloofarkheirkhah/nili
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/niloofarkheirkhah/nili && cd nili
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 nili.py -t 10.0.0.0/24` | 网络扫描+中间人 |
| `-t cidr -s` | 嗅探 |
| `-t cidr -d` | ARP 欺骗 |

## 攻击场景 Playbook

### 扫描+MITM 一体

```bash
python3 nili.py -t 10.0.0.0/24 -s
# 轻量内网工具
```

## 注意事项

网络扫描+中间人综合工具。
