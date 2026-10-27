---
name: wcvs-web-cache-vuln
description: Web Cache Vulnerability Scanner (wcvs): 缓存投毒探测。信号:web漏洞,注入,Web 缓存漏洞扫描,包含缓存投毒,自定义字典。
---

# Web Cache Vulnerability Scanner (wcvs)

- 攻击大类:C09 Web利用(缓存投毒)
- 上游仓库:https://github.com/Hackmanit/Web-Cache-Vulnerability-Scanner
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/Hackmanit/Web-Cache-Vulnerability-Scanner@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `wcvs -u 'https://t.com'` | Web 缓存漏洞扫描 |
| `-u url -sp -sm` | 包含缓存投毒 |
| `-u url -d wordlist.txt` | 自定义字典 |
| `-o report.html` | HTML 报告 |

## 攻击场景 Playbook

### 缓存投毒探测

```bash
wcvs -u 'https://t.com' -sp
# 检测缓存键处理缺陷与投毒可行性
```

## 注意事项

检测 Web 缓存投毒/欺骗(伪 URL、HTTP 头投毒、Cookie 投毒)。Hackmanit 学术团队出品。
