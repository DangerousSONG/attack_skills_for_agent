---
name: above-protocol-anomaly
description: 渗透工具 skill:Above 的安装、参数速查与攻击场景 playbook。当任务涉及 嗅探与中间人攻击 需要调用 Above 时使用。
when-to-use: 渗透工具 skill:Above 的安装、参数速查与攻击场景 playbook。当任务涉及 嗅探与中间人攻击 需要调用 Above 时使用。
---

# Above

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/caster0x00/Above
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/caster0x00/Above && cd Above
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 above.py -i eth0 -F` | 协议异常检测 |
| `-i eth0 -d` | ARP 欺骗 |
| `-i eth0 -p` | PCAP 分析 |

## 攻击场景 Playbook

### 内网协议层攻击检测

```bash
python3 above.py -i eth0 -d
# 抓取异常协议行为(中间人/扫描)
```

## 注意事项

协议层异常检测,发现内网攻击行为。
