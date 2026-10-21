---
name: dnssearch-enum
description: 渗透工具 skill:dnsSearch 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 dnsSearch 时使用。
when-to-use: 渗透工具 skill:dnsSearch 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 dnsSearch 时使用。
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
