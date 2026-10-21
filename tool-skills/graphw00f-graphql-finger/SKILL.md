---
name: graphw00f-graphql-finger
description: 渗透工具 skill:graphw00f 的安装、参数速查与攻击场景 playbook。当任务涉及 API与GraphQL攻击 需要调用 graphw00f 时使用。
when-to-use: 渗透工具 skill:graphw00f 的安装、参数速查与攻击场景 playbook。当任务涉及 API与GraphQL攻击 需要调用 graphw00f 时使用。
---

# graphw00f

- 攻击大类:C10 API与GraphQL攻击
- 上游仓库:https://github.com/dolevf/graphw00f
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/dolevf/graphw00f && cd graphw00f && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 main.py -d -t https://t.com/graphql` | GraphQL 引擎指纹识别 |
| `-f` | 指纹库全检测 |
| `-p` | 仅探测 GraphQL 端点 |

## 攻击场景 Playbook

### GraphQL 端点定位+技术栈

```bash
python3 main.py -d -t https://t.com/api
# 识别 Apollo/Hasura/Lighthouse 等引擎,对着对应 CVE 打
```

## 注意事项

GraphQL 服务器指纹库,识别后按引擎查已知漏洞(如旧版 Apollo 的调试接口)。
