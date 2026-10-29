---
name: armscgen-shellcode
description: "ARMSCGen: generates ARM/embedded shellcode. Signals: pwn, binary exploitation, reverse shell, list"
zh-signals: "ARMSCGen: ARM/嵌入式 shellcode。信号:pwn,二进制利用,反向 shell,列表。"
---

# ARMSCGen

- 攻击大类:C46 二进制漏洞利用与Pwn
- 上游仓库:https://github.com/alexpark07/ARMSCGen
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/alexpark07/ARMSCGen
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 ARMSCGen.py -f sc_flimsy` | ARM shellcode 生成 |
| `-f sc_reverse_tcp` | 反向 shell |
| `-l` | 列表 |

## 攻击场景 Playbook

### ARM/嵌入式 shellcode

```bash
python3 ARMSCGen.py -f sc_egghunter
# ARM 架构 shellcode
```

## 注意事项

ARM shellcode 生成器。
