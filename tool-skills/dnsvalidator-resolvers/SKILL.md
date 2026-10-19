---
name: dnsvalidator-resolvers
description: 渗透工具 skill:dnsvalidator 的安装、参数速查与攻击场景 playbook。当任务涉及 域名与DNS侦察 需要调用 dnsvalidator 时使用。
---

# dnsvalidator

- 攻击大类:C02 域名与DNS侦察
- 上游仓库:https://github.com/vortexau/dnsvalidator
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/vortexau/dnsvalidator && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 dnsvalidator.py -tL public_resolvers.txt -o valid.txt` | 验证 DNS 解析器 |
| `-tL file -threads 100` | 线程 |
| `-c 500` | 并发 |

## 攻击场景 Playbook

### 构建干净 resolver 池

```bash
python3 dnsvalidator.py -tL resolvers.txt -o clean.txt
# 子域爆破前必备,剔除毒化 resolver
```

## 注意事项

DNS 解析器清洗工具,amass/shuffledns 前置。
