---
name: nray-distributed-scan
description: "Massive-scale port scanning. Signals: port scanning, nmap, distributed port scanning, rate, JSON output."
zh-signals: "nray: 超大规模端口扫描。信号:端口扫描,nmap,分布式端口扫描,速率,JSON 输出。"
---

# nray

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/nray-scanner/nray
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/nray-scanner/nray@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `nray -targets 10.0.0.0/24 -p 1-10000` | 分布式端口扫描 |
| `-targets cidr -rate 5000` | 速率 |
| `-o out.json` | JSON 输出 |
| `-workers 100` | 分布式节点 |

## 攻击场景 Playbook

### 超大规模端口扫描

```bash
nray -targets 10.0.0.0/8 -p top1000 -rate 10000
# 分布式架构,比 nmap 快一个量级
```

## 注意事项

事件驱动端口扫描,支持分布式,大数据量场景。
