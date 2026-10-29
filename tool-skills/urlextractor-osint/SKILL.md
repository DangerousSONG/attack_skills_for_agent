---
name: urlextractor-osint
description: "URLextractor: Target URL intelligence aggregation. Signals: web vulnerabilities, injection, target OSINT extraction, include subdomains, with port scan."
zh-signals: "URLextractor: 目标 URL 情报聚合。信号:web漏洞,注入,目标 OSINT 提取,包含子域,含端口扫描。"
---

# URLextractor

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/eschultze/URLextractor
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/eschultze/URLextractor && cd URLextractor
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./extractor.sh t.com` | 目标 OSINT 提取 |
| `-d t.com -s` | 包含子域 |
| `-d t.com -p` | 含端口扫描 |

## 攻击场景 Playbook

### 目标 URL 情报聚合

```bash
./extractor.sh corp.com
# 多源收 URL+IP+技术栈
```

## 注意事项

多源 OSINT URL 收集,带技术栈识别。
