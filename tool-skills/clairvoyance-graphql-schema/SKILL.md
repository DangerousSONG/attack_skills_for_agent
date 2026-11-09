---
name: clairvoyance-graphql-schema
description: "clairvoyance: Collects information from introspection-disabled GraphQL. Signals: API attack, interface testing, authenticated requests, dictionary enhancement."
zh-signals: "clairvoyance: 关闭内省的 GraphQL 信息收集。信号:api攻击,接口测试,带认证,字典增强。"
---

# clairvoyance

- 攻击大类:C10 API与业务逻辑攻击
- 上游仓库:https://github.com/nikitastupin/clairvoyance
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install clairvoyance
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python -m clairvoyance https://t.com/graphql -o schema.json` | 关 introspection 时还原 schema |
| `-H 'Authorization: Bearer x'` | 带认证 |
| `-w wordlist.txt` | 字典增强 |

## 攻击场景 Playbook

### 关闭内省的 GraphQL 信息收集

```bash
python -m clairvoyance https://api.target.com/graphql -o schema.graphql
# 通过字段猜测+错误信息差异重建完整 schema
```

## 注意事项

introspection 被禁时的 schema 重建;输出可直接导入 GraphQLmap/Burp。
