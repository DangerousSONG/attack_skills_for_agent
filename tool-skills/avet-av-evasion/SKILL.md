---
name: avet-av-evasion
description: AVET: 杀软环境载荷投递。信号:恶意软件开发,免杀开发,交互式载荷构建,编码选择,列出编码器。
---

# AVET

- 攻击大类:C45 免杀与载荷投递
- 上游仓库:https://github.com/govolution/avet
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/govolution/avet && cd avet && bash setup.sh
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `bash build/build_win32_meterpreter_rev_tcp.sh` | 生成 shellcode 载荷 |
| `./avet_fabric.py` | 交互式载荷构建 |
| `--encoder xor` | 编码选择 |
| `-l` | 列出编码器 |

## 攻击场景 Playbook

### 杀软环境载荷投递

```bash
bash avet_fabric.py
# 选 payload+编码组合,输出 exe,VT 查杀率比裸 msfvenom 低
```

## 注意事项

反病毒逃逸工具集,多种编码/加壳/分离式载荷构建,对抗静态查杀。
