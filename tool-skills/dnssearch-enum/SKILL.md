---
name: dnssearch-enum
description: "dnsSearch: lightweight fast subdomain brute-forcing. Signals: asset mapping, subdomain, resolver, threads."
zh-signals: "dnsSearch: 快速子域爆破轻量件。信号:资产测绘,子域名,resolver,线程。"
---

# dnsSearch

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/ptrrkssn/dnssearch
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/ptrrkssn/dnssearch && cd dnssearch && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `dnssearch -d corp.com -w wordlist.txt` | 子域爆破 |
| `-r resolvers.txt` | resolver |
| `-t 20` | 线程 |

## 攻击场景 Playbook

### 快速子域爆破轻量件

```bash
dnssearch -d corp.com -w subs.txt -r resolvers.txt
```

## 注意事项

C 写的小工具,资源占用极低,适合在跳板机上跑。
