---
name: subjack-takeover
description: "subjack batch-filters dangling subdomain takeovers. Signals: subdomain, domain enumeration, batch takeover detection, threads, timeout"
zh-signals: "subjack: dangling 子域接管批量筛。信号:子域名,域名枚举,批量检测接管,线程,超时。"
---

# subjack

- 攻击大类:C02 域名与DNS侦察
- 上游仓库:https://github.com/haccer/subjack
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/haccer/subjack@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `-w subs.txt` | 批量检测接管 |
| `-t 20` | 线程 |
| `-timeout 30` | 超时 |
| `-o results.txt` | 输出 |
| `-ssl` | HTTPS 指纹 |
| `-c fingerprints.json` | 自定义指纹 |
| `-v` | 详细 |

## 攻击场景 Playbook

###  dangling 子域接管批量筛

```bash
subfinder -d corp.com | subjack -w - -t 50 -o takeover.txt -ssl
# 命中即显示 service+fingerprint,如 S3/GitHub Pages
```

## 注意事项

Go 编写速度快;接管指纹覆盖 30+ 服务(S3/Heroku/Github/Shopify 等)。
