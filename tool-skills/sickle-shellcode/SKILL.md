---
name: sickle-shellcode
description: Sickle: shellcode 分析。信号:逆向,反汇编,坏字符,对比。
---

# Sickle

- 攻击大类:C47 逆向工程
- 上游仓库:https://github.com/wetw0rk/Sickle
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/wetw0rk/Sickle && cd Sickle && pip install .
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `sickle -f shellcode.bin -m disassemble` | shellcode 反汇编 |
| `-f bin -f badchars '\x00'` | 坏字符 |
| `-m diff` | 对比 |

## 攻击场景 Playbook

### shellcode 分析

```bash
sickle -f payload.bin -m disassemble
# 反汇编+坏字符检测
```

## 注意事项

shellcode 分析工具,反汇编+提取。
