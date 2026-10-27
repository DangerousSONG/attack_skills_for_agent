---
name: interlace-parallel
description: Interlace: 渗透命令并行化。信号:红队,方法论,并行命令执行,占位符,端口列表。
---

# Interlace

- 攻击大类:C50 红队方法论与自动化
- 上游仓库:https://github.com/codingo/Interlace
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install interlace
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `interlace -tL targets.txt -threads 5 -c 'nmap {{target}}'` | 并行命令执行 |
| `-c 'cmd _target_ _port_'` | 占位符 |
| `-pL ports.txt` | 端口列表 |

## 攻击场景 Playbook

### 渗透命令并行化

```bash
interlace -tL ips.txt -threads 20 -c 'nmap -sV {{target}} -oN scans/_target_.nmap'
# 单命令变并行任务
```

## 注意事项

渗透命令并行调度器,codingo 出品。
