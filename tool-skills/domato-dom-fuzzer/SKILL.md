---
name: domato-dom-fuzzer
description: 渗透工具 skill:Domato 的安装、参数速查与攻击场景 playbook。当任务涉及 模糊测试与漏洞挖掘 需要调用 Domato 时使用。
when-to-use: 渗透工具 skill:Domato 的安装、参数速查与攻击场景 playbook。当任务涉及 模糊测试与漏洞挖掘 需要调用 Domato 时使用。
---

# Domato

- 攻击大类:C46 模糊测试与漏洞挖掘
- 上游仓库:https://github.com/googleprojectzero/domato
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/googleprojectzero/domato
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python generator.py --output_dir out/ --no_of_files 100` | 生成 HTML fuzz 样本 |
| `--grammar grammar.txt` | 自定义语法 |
| `python fuzzer.py out/ target` | 喂给目标 |

## 攻击场景 Playbook

### 浏览器/DOM 引擎 fuzz

```bash
python generator.py --output_dir cases/ --no_of_files 500
# Project Zero 出品,语法感知样本,挖渲染器 UAF
```

## 注意事项

Google Project Zero 出品的 DOM fuzzer,语法感知的样本生成,曾挖大量浏览器 CVE。
