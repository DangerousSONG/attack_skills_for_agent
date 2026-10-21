---
name: subscraper-subdomains
description: 渗透工具 skill:SubScraper 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 SubScraper 时使用。
when-to-use: 渗透工具 skill:SubScraper 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 SubScraper 时使用。
---

# SubScraper

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/m8sec/subscraper
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install subscraper
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `subscraper target.com` | 被动+DNS 记录枚举 |
| `-r` | DNS 记录解析 |
| `-o subs.txt` | 输出 |
| `-t 30` | 线程 |

## 攻击场景 Playbook

### DNS 记录深挖子域

```bash
subscraper corp.com -r -o subs.txt  # 从 MX/NS/SPF/CNAME 记录关联子域
```

## 注意事项

特色是从 DNS 记录关联而非纯字典;与证书透明度互补。
