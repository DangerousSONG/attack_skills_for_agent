---
name: second-order-subdomain-takeover
description: 渗透工具 skill:second-order 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 second-order 时使用。
when-to-use: 渗透工具 skill:second-order 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 second-order 时使用。
---

# second-order

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/mhmdiaa/second-order
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/mhmdiaa/second-order@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `second-order -t https://t.com -w wordlist.txt` | 子域接管检测 |
| `-t url -c amazon,azure` | 指定云服务 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 子域接管批量扫描

```bash
second-order -t subs.txt -w providers.txt
#  dangling CNAME 检测 20+ 云服务商
```

## 注意事项

子域接管(subdomain takeover)扫描,检测悬空的 DNS 记录。
