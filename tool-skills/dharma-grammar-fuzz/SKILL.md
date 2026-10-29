---
name: dharma-grammar-fuzz
description: "dharma: protocol/file format fuzz sample generation. Signals: pwn, binary exploitation, syntax-based sample generation, counter mode, debugging."
zh-signals: "dharma: 协议/文件格式 fuzz 样本生成。信号:pwn,二进制利用,按语法生成样本,计数器模式,调试。"
---

# dharma

- 攻击大类:C46 模糊测试与漏洞挖掘
- 上游仓库:https://github.com/MozillaSecurity/dharma
- 上游 License:MPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/MozillaSecurity/dharma && cd dharma && pip install .
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python dharma.py -g grammars/dom.dg -n 100` | 按语法生成样本 |
| `-c 4` | 计数器模式 |
| `--loglevel debug` | 调试 |

## 攻击场景 Playbook

### 协议/文件格式 fuzz 样本生成

```bash
python dharma.py -g grammars/css.dg -n 1000 > cases.txt
# Mozilla 出品,模板语法生成高覆盖样本
```

## 注意事项

Mozilla 语法 fuzz 框架,用 .dg 语法描述格式生成样本,配 AFL 类引擎使用。
