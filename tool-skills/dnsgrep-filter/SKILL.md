---
name: dnsgrep-filter
description: 渗透工具 skill:dnsgrep 的安装、参数速查与攻击场景 playbook。当任务涉及 域名与DNS侦察 需要调用 dnsgrep 时使用。
when-to-use: 渗透工具 skill:dnsgrep 的安装、参数速查与攻击场景 playbook。当任务涉及 域名与DNS侦察 需要调用 dnsgrep 时使用。
---

# dnsgrep

- 攻击大类:C02 域名与DNS侦察
- 上游仓库:https://github.com/erbbysam/dnsgrep
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/erbbysam/dnsgrep && cd dnsgrep && go build
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `cat big_dns.txt | ./dnsgrep -f corp.com` | DNS 数据过滤 |
| `-f domain -o out.txt` | 输出 |
| `-r regex` | 正则 |

## 攻击场景 Playbook

### 海量 DNS 数据筛目标

```bash
cat rapid7_dns.txt | ./dnsgrep -f '\.corp\.com'
# 数据集内挖目标子域
```

## 注意事项

快速过滤大型 DNS 数据集(CERT 数据集等)。
