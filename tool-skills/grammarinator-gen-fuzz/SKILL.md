---
name: grammarinator-gen-fuzz
description: 渗透工具 skill:grammarinator 的安装、参数速查与攻击场景 playbook。当任务涉及 模糊测试与漏洞挖掘 需要调用 grammarinator 时使用。
when-to-use: 渗透工具 skill:grammarinator 的安装、参数速查与攻击场景 playbook。当任务涉及 模糊测试与漏洞挖掘 需要调用 grammarinator 时使用。
---

# grammarinator

- 攻击大类:C46 模糊测试与漏洞挖掘
- 上游仓库:https://github.com/renatahodovan/grammarinator
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install grammarinator
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `grammarinator-process grammar.g4 -o out/` | 从 ANTLR 语法生成生成器 |
| `grammarinator-generate -l out/Generator.py -r out/unparser.py -o tests/ -n 100` | 生成测试样本 |
| `grammarinator-parse ...` | 解析已有样本变异 |

## 攻击场景 Playbook

### ANTLR 语法驱动 fuzz

```bash
grammarinator-process JavaScript.g4 -o gen/ && grammarinator-generate -l gen/ -o cases/ -n 500
# 任意 ANTLR 语法转成 fuzz 生成器
```

## 注意事项

ANTLR 语法自动生成 fuzz 样本,无需手写生成器,覆盖面高于随机变异。
