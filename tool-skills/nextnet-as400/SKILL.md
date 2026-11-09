---
name: nextnet-as400
description: "nextnet: ICS/legacy system discovery. Signals: port scanning, nmap, special protocol discovery, AS400 scanning."
zh-signals: "nextnet: 工控/遗留系统发现。信号:端口扫描,nmap,特殊协议发现,AS400 扫描。"
---

# nextnet

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/hdm/nextnet
- 上游 License:BSD-2-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/hdm/nextnet@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `nextnet -p 1-10000 10.0.0.0/24` | 特殊协议发现 |
| `-p ports -s as400` | AS400 扫描 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 工控/遗留系统发现

```bash
nextnet 10.0.0.0/16
# hdm 出品,发现非标准协议设备
```

## 注意事项

hdm 出品,遗留系统/工控协议发现。
