---
name: snscrape-social
description: "snscrape: reconstructs target social footprint and timeline. Signals: email collection, employee info, fetch user tweets, search syntax, single tweet."
zh-signals: "snscrape: 目标社交足迹与时间线重建。信号:邮箱收集,员工信息,拉取用户推文,搜索语法,单条推文。"
---

# snscrape

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/JustAnotherArchivist/snscrape
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install snscrape
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `snscrape --jsonl twitter-user target > t.jsonl` | 拉取用户推文 |
| `twitter-search 'from:user since:2023-01-01'` | 搜索语法 |
| `twitter-tweet url` | 单条推文 |
| `instagram-user user` | IG 公开资料(受限) |

## 攻击场景 Playbook

### 目标社交足迹与时间线重建

```bash
snscrape --jsonl twitter-user victim | jq -r '.content' | head -100
# 定位工作地点/同事关系/密码提示类信息
```

## 注意事项

纯被动抓取公开页;Twitter 接口变动频繁,失效时换 --max-results 小步试。
