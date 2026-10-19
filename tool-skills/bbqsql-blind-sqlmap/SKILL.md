---
name: bbqsql-blind-sqlmap
description: 渗透工具 skill:BBQSQL 的安装、参数速查与攻击场景 playbook。当任务涉及 Web利用(SQL注入) 需要调用 BBQSQL 时使用。
---

# BBQSQL

- 攻击大类:C09 Web利用(SQL注入)
- 上游仓库:https://github.com/neohapsis/bbqsql
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install bbqsql
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `bbqsql` | 进入交互配置: URL/方法/注入点/对比请求 |
| `run` | 配置完成后执行盲注 |
| `export results.csv` | 导出结果 |

## 攻击场景 Playbook

### 半盲注手工配置

```bash
bbqsql
# set url=https://t.com/report?id=1; injection point 选 id; technique=comparison; run
```

## 注意事项

SQL 盲注框架,适合 sqlmap 打不动的自定义对比逻辑(如两个响应相似度)。交互式配置菜单驱动。
