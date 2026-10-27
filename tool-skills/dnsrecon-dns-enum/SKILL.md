---
name: dnsrecon-dns-enum
description: dnsrecon: SRV 记录挖内部服务、Zone Transfer 尝试。信号:子域名,域名枚举,标准枚举,字典爆破。
---

# dnsrecon

- 攻击大类:C02 域名与DNS侦察
- 上游仓库:https://github.com/darkoperator/dnsrecon
- 上游 License:LGPL-2.1(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install dnsrecon 或 pip install dnsrecon
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `-d target.com` | 标准枚举 |
| `-t axfr` | zone transfer 检测 |
| `-t brt -D wordlist` | 字典爆破 |
| `-t srv` | SRV 记录枚举 |
| `-t rvl` | 反向解析 |
| `--csv out.csv` | CSV 输出 |
| `--threads 10` | 线程 |

## 攻击场景 Playbook

### SRV 记录挖内部服务

```bash
dnsrecon -d corp.com -t srv --csv srv.csv
# 输出 _ldap._tcp 等 → 定位域控/邮件/会议服务
```

### Zone Transfer 尝试

```bash
dnsrecon -d target.com -t axfr
```

## 注意事项

dnsenum 的 Python 增强版,SRV 枚举对 AD 环境价值高;XML/CSV 输出便于管道。
