---
name: second-order-subdomain-takeover
description: second-order: 子域接管批量扫描。信号:web漏洞,注入,子域接管检测,指定云服务。
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
