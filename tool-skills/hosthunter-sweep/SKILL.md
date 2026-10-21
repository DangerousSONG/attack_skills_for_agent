---
name: hosthunter-sweep
description: 渗透工具 skill:HostHunter 的安装、参数速查与攻击场景 playbook。当任务涉及 网络拓扑与互联网测绘 需要调用 HostHunter 时使用。
when-to-use: 渗透工具 skill:HostHunter 的安装、参数速查与攻击场景 playbook。当任务涉及 网络拓扑与互联网测绘 需要调用 HostHunter 时使用。
---

# HostHunter

- 攻击大类:C04 网络拓扑与互联网测绘
- 上游仓库:https://github.com/SpiderLabs/HostHunter
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/SpiderLabs/HostHunter && cd HostHunter
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 hosthunter.py 10.0.0.5 10.0.0.6` | OSINT 主机名发现 |
| `-f targets.txt` | 批量 |
| `-o out.csv` | 输出 |

## 攻击场景 Playbook

### IP→主机名 OSINT

```bash
python3 hosthunter.py 1.2.3.4 5.6.7.8
# 证书透明度+在线源反查
```

## 注意事项

SpiderLabs 出品,目标 IP 主机名发现。
