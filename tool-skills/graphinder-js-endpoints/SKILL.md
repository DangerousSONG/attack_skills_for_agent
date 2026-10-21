---
name: graphinder-js-endpoints
description: 渗透工具 skill:Graphinder 的安装、参数速查与攻击场景 playbook。当任务涉及 外部攻击面与云资产暴露 需要调用 Graphinder 时使用。
when-to-use: 渗透工具 skill:Graphinder 的安装、参数速查与攻击场景 playbook。当任务涉及 外部攻击面与云资产暴露 需要调用 Graphinder 时使用。
---

# Graphinder

- 攻击大类:C05 外部攻击面与云资产暴露
- 上游仓库:https://github.com/EscuelaTechnica/graphinder
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install graphinder
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `graphinder -d corp.com` | JS 中 GraphQL 端点发现 |
| `-d domain -s` | 子域联动 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 隐藏 GraphQL 端点发现

```bash
graphinder -d corp.com
# JS bundle 里翻 /graphql 端点
```

## 注意事项

JS 文件中 GraphQL/Apollo 端点提取。
