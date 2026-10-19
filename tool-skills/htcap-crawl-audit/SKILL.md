---
name: htcap-crawl-audit
description: 渗透工具 skill:htcap 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 htcap 时使用。
---

# htcap

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/segment-srl/htcap
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/segment-srl/htcap && cd htcap
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python htcap.py -w urls.txt -o db.sqlite https://t.com` | 爬取+存 SQLite |
| `python htcap.py --assess db.sqlite` | 漏洞评估 |
| `-x 3` | 爬深 |
| `-p 20` | 并发 |

## 攻击场景 Playbook

### Ajax 站点全量爬取

```bash
python htcap.py https://t.com -o t.sqlite
# 无头浏览器爬 SPA,产出漏洞评估数据库
```

## 注意事项

segment 出品的爬虫,专门处理 Ajax/JS 重度站点,输出结构化可查询。
