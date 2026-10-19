---
name: shellnoob-shellcode
description: 渗透工具 skill:shellnoob 的安装、参数速查与攻击场景 playbook。当任务涉及 载荷开发与武器化 需要调用 shellnoob 时使用。
---

# shellnoob

- 攻击大类:C07 载荷开发与武器化
- 上游仓库:https://github.com/reyammer/shellnoob
- 上游 License:BSD-2-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install shellnoob 或 git clone https://github.com/reyammer/shellnoob
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `shellnoob -c 'exec /bin/sh'` | shellcode 汇编互转 |
| `-i shellcode.txt` | 反汇编 |
| `-f input.txt -o output` | 格式转换 |
| `-32 / -64` | 架构 |

## 攻击场景 Playbook

### 汇编↔shellcode 快速互转

```bash
shellnoob -c 'xor eax,eax; push 0x68732f2f; push 0x6e69622f; mov ebx,esp; ...'
# 教学/CTF 调 shellcode 方便
```

## 注意事项

老牌教学工具,Python2 时代作品;复杂 shellcode 建议用 nasm+objdump 或 pwntools。
