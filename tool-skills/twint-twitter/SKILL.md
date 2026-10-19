---
name: twint-twitter
description: 渗透工具 skill:twint 的安装、参数速查与攻击场景 playbook。当任务涉及 邮箱与人员OSINT 需要调用 twint 时使用。
---

# twint

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/twintproject/twint
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip3 install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `twint -u username -o out.csv --csv` | 拉取用户全部推文 |
| `-s 'keyword'` | 关键词搜索 |
| `--since 2023-01-01 --until 2023-06-01` | 时间窗 |
| `-u user --followers` | 粉丝列表 |
| `--email --phone` | 筛留联系方式的推文 |

## 攻击场景 Playbook

### 目标账号全量考古

```bash
twint -u victim -o tweets.csv --csv
# 配合 grep -iE 'password|vpn|internal|@corp' 挖敏感自曝信息
```

## 注意事项

无 API key 抓取,接口失效时换 --retweets 或自建 cookie;快照型工具,可用性随 X 平台策略变化。
