---
name: dnsmap-subdomain
description: 渗透工具 skill:dnsmap 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 dnsmap 时使用。
when-to-use: 渗透工具 skill:dnsmap 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 dnsmap 时使用。
---

# dnsmap

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/resurrecting-open-source-projects/dnsmap
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install dnsmap
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `dnsmap target.com` | 子域爆破 |
| `-w wordlist` | 自定义字典 |
| `-r out.txt` | 结果文件 |
| `-i ipskip.txt` | 忽略 IP |

## 攻击场景 Playbook

### 快速子域初筛

```bash
dnsmap corp.com -r subs.txt
```

## 注意事项

轻量子域爆破;字典内置,零配置直接跑。
