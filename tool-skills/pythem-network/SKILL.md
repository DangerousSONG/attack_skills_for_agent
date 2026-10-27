---
name: pythem-network
description: PytheM: 网络渗透一体化。信号:中间人,mitm,网络攻击框架,ARP 欺骗,嗅探。
---

# PytheM

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/m4n3dw0lf/PytheM
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/m4n3dw0lf/PytheM && cd PytheM && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 pythem.py -i eth0` | 网络攻击框架 |
| `-i eth0 -arpspoof` | ARP 欺骗 |
| `-i eth0 - sniff` | 嗅探 |
| `-i eth0 - brute ssh` | 爆破 |

## 攻击场景 Playbook

### 网络渗透一体化

```bash
python3 pythem.py -i eth0
# ARP/DNS/嗅探/爆破 一体
```

## 注意事项

Python 网络渗透多合一框架。
