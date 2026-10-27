---
name: bluffy-hollow
description: bluffy: shellcode 免杀。信号:恶意软件开发,免杀开发,shellcode 混淆,AES 加密,直接 syscall。
---

# bluffy

- 攻击大类:C45 恶意软件开发与免杀
- 上游仓库:https://github.com/ad-995/bluffy
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/ad-995/bluffy && cd bluffy
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 bluffy.py -f payload.bin -e xor` | shellcode 混淆 |
| `-f bin -e aes` | AES 加密 |
| `-f bin -s syscalls` | 直接 syscall |

## 攻击场景 Playbook

### shellcode 免杀

```bash
python3 bluffy.py -f beacon.bin -e chacha20
# 落地前混淆
```

## 注意事项

shellcode 混淆+syscall 直接执行。
