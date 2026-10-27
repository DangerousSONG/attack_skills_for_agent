---
name: graphqlmap-graphql
description: GraphQLmap: GraphQL 接口攻击面枚举。信号:api攻击,接口测试,交互模式,NoSQL 注入测试,测试 mutation。
---

# GraphQLmap

- 攻击大类:C10 API与业务逻辑攻击
- 上游仓库:https://github.com/swisskyrepo/GraphQLmap
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/swisskyrepo/GraphQLmap && cd GraphQLmap && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python graphqlmap.py -u https://t.com/graphql` | 交互模式 |
| `dump_new` | 导出 schema 与接口 |
| `nosqli` | NoSQL 注入测试 |
| `postgresqli` | SQL 注入测试 |
| `mutation` | 测试 mutation |
| `intent` | 见上游文档 |
| `越权探测` | 见上游文档 |

## 攻击场景 Playbook

### GraphQL 接口攻击面枚举

```bash
python graphqlmap.py -u https://api.target.com/graphql
GraphQLmap > dump_new  # 全部 type/query/mutation 导出
GraphQLmap > nosqli  # 参数注入测试
```

## 注意事项

交互式 GraphQL 渗透;dump 出的接口面直接指导越权与注入测试。
