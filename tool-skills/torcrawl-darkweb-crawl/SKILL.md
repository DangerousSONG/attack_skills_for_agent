---
name: torcrawl-darkweb-crawl
description: 渗透工具 skill:TorCrawl 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 TorCrawl 时使用。
---

# TorCrawl

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/MikeMeliz/TorCrawl.py
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/MikeMeliz/TorCrawl.py && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 torcrawl.py -u http://target.onion` | 暗网站点爬取 |
| `-u url -c` | 爬取链接 |
| `-u url -e` | 提取邮箱 |
| `-d 2` | 深度 |

## 攻击场景 Playbook

### 暗网站点结构化提取

```bash
python3 torcrawl.py -u http://leak.onion -e -d 3
# 暗网数据泄露站批量提取
```

## 注意事项

Tor 网络爬虫,自动过 Tor 代理爬取 .onion 站点。
