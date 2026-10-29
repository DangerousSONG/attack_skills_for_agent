---
name: sandsifter-cpu-fuzz
description: "sandsifter: Discovers CPU instruction side channels and vulnerabilities. Signals: pwn, binary exploitation, scan undocumented instructions, disassembly differences, pattern scanning."
zh-signals: "sandsifter: CPU 指令集差异侧信道/漏洞挖掘。信号:pwn,二进制利用,扫描未文档指令,反汇编差异,模式扫描。"
---

# sandsifter

- 攻击大类:C46 二进制漏洞利用与Pwn
- 上游仓库:https://github.com/xoreaxeaxeax/sandsifter
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/xoreaxeaxeax/sandsifter && cd sandsifter && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./sifter.py --unk` | 扫描未文档指令 |
| `--dis` | 反汇编差异 |
| `--tick` | 模式扫描 |
| `--raw` | 原始字节 |
| `-p 0` | 从 0 字节长开始 |

## 攻击场景 Playbook

### CPU 指令集差异侧信道/漏洞挖掘

```bash
sudo ./sifter.py --unk --dis
# 找出 CPU 执行与文档不一致的指令(可用于混淆或漏洞研究)
```

## 注意事项

需 root(kernel module);仅研究用途,跑前保存现场。
