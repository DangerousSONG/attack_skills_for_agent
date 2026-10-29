---
name: astra-api-scan
description: "Astra: batch scans REST API vulnerabilities. Signals: api attack, interface testing, REST API scan, JSON report, API-only mode"
zh-signals: "Astra: REST API 漏洞批扫。信号:api攻击,接口测试,REST API 扫描,JSON 报告,仅 API 模式。"
---

# Astra

- 攻击大类:C10 API与业务逻辑攻击
- 上游仓库:https://github.com/flipkart-incubator/Astra
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/flipkart-incubator/Astra && cd Astra && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python astra.py -u https://t.com/api -m scan` | REST API 扫描 |
| `-H 'Authorization: Bearer x'` | 头 |
| `-m scan -o json` | JSON 报告 |
| `-u URL -m api` | 仅 API 模式 |

## 攻击场景 Playbook

### REST API 漏洞批扫

```bash
python astra.py -u https://api.target.com -m scan
# 输出 OWASP API Top10 各项结果(鉴权/SQLi/XSS/信息泄露)
```

## 注意事项

Flipkart 出品的 API 扫描;覆盖 OWASP API Security Top 10。
