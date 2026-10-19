---
name: preeny-pwn
description: 渗透工具 skill:preeny 的安装、参数速查与攻击场景 playbook。当任务涉及 二进制漏洞利用与Pwn 需要调用 preeny 时使用。
---

# preeny

- 攻击大类:C46 二进制漏洞利用与Pwn
- 上游仓库:https://github.com/zardus/preeny
- 上游 License:BSD-2-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/zardus/preeny && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `LD_PRELOAD=./desock.so ./chroot` | socket→stdio 转换 |
| `LD_PRELOAD=./defork.so ./bin` | 去 fork |
| `LD_PRELOAD=./slow.o ./bin` | 延时(暴力防提速) |

## 攻击场景 Playbook

### CTF/自动化 pwn 辅助

```bash
LD_PRELOAD=./desock.so ./target  # socket 程序变 stdin 交互,直接 pipe payload
```

## 注意事项

pwn 常用 LD_PRELOAD 补丁集;CTF 自动化与 fuzz 降速都靠它。
