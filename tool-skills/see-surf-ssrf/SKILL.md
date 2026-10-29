---
name: see-surf-ssrf
description: "See-SURF: crawling plus SSRF dual probing. Signals: web vulnerability, injection, crawl-based SSRF detection, OOB callback, concurrency."
zh-signals: "See-SURF: 爬取+SSRF 双探测。信号:web漏洞,注入,SSRF 爬取式检测,OOB 回调,并发。"
---

# See-SURF

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/In3tinct/See-SURF
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/In3tinct/See-SURF && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 see-surf.py -u https://t.com` | SSRF 爬取式检测 |
| `-u url -b http://burp.collab` | OOB 回调 |
| `-c 20` | 并发 |
| `-w urls.txt` | 批量 |

## 攻击场景 Playbook

### 爬取+SSRF 双探测

```bash
python3 see-surf.py -u https://t.com -b http://vps.oob.sh
# 先爬全站再对参数打 SSRF
```

## 注意事项

Python3+Selenium 爬取目标后对全部 URL 参数做 SSRF 注入。
