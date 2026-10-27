---
name: vhostscan-virtual-host
description: VHostScan: 共享 IP 虚拟主机发现。信号:端口扫描,nmap,虚拟主机枚举,SSL。
---

# VHostScan

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/codingo/VHostScan
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install vhostscan
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `vhostscan -t 10.0.0.5 -w vhosts.txt` | 虚拟主机枚举 |
| `-t ip -p 443 --ssl` | SSL |
| `-oN out.txt` | 输出 |
| `--fuzzy-logic` | 模糊匹配 |

## 攻击场景 Playbook

### 共享 IP 虚拟主机发现

```bash
vhostscan -t 10.0.0.5 -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
# 发现同一 IP 上的隐藏站点
```

## 注意事项

虚拟主机发现工具,基于 Host 头枚举。
