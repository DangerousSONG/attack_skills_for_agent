---
name: reconnoitre-auto-recon
description: 渗透工具 skill:reconnoitre 的安装、参数速查与攻击场景 playbook。当任务涉及 红队方法论与自动化 需要调用 reconnoitre 时使用。
---

# reconnoitre

- 攻击大类:C50 红队方法论与自动化
- 上游仓库:https://github.com/codingo/Reconnoitre
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/codingo/Reconnoitre && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 reconnoitre.py -t 10.0.0.0/24 -o out/ --services` | 服务枚举 |
| `-t cidr -o out --dns` | DNS 枚举 |
| `-t cidr -o out --perform` | 全量 |
| `--snmp` | SNMP 枚举 |

## 攻击场景 Playbook

### 内网自动侦察

```bash
python3 reconnoitre.py -t 10.0.0.0/24 -o enum/ --perform
# 目录结构+服务+DNS 自动归档,codingo 出品
```

## 注意事项

内网自动化侦察框架,输出按主机归档。
