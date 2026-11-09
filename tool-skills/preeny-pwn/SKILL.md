---
name: preeny-pwn
description: "CTF/automated pwn assistance. Signals: pwn, binary exploitation, disable fork, delay to prevent brute-force speedup."
zh-signals: "preeny: CTF/自动化 pwn 辅助。信号:pwn,二进制利用,去 fork,延时(暴力防提速)。"
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
