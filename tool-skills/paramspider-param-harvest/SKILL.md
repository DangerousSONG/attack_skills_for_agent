---
name: paramspider-param-harvest
description: ParamSpider: 带参 URL 批量收割(喂漏洞扫描器)。信号:数据收集,打包,高爬取深度,排除扩展。
---

# ParamSpider

- 攻击大类:C33 URL与内容发现
- 上游仓库:https://github.com/devanshbatham/ParamSpider
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/devanshbatham/ParamSpider && cd ParamSpider && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 paramspider.py -d target.com` | 从 Web 存档提取带参 URL |
| `-d target.com -l high` | 高爬取深度 |
| `-e php,aspx` | 排除扩展 |
| `-o params.txt` | 输出 |

## 攻击场景 Playbook

### 带参 URL 批量收割(喂漏洞扫描器)

```bash
python3 paramspider.py -d corp.com -l high -o urls.txt
# 交 dalfox/sqlmap 批量打 XSS/SQLi
```

## 注意事项

从 Wayback/常见爬源提取目标域带参数的 URL,免去手工翻存档,自动化漏扫前置神器。
