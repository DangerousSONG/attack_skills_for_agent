---
name: ciphr-crypto-cli
description: "ciphr: Performs cryptographic operations from the command line. Signals: cryptographic attack, encryption cracking, ciphr --hex, hash calculation, AES decryption."
zh-signals: "ciphr: 命令行密码学运算。信号:密码学攻击,加密破解,ciphr --hex`,哈希计算,AES 解密。"
---

# ciphr

- 攻击大类:C49 密码学攻击
- 上游仓库:https://github.com/frohoff/ciphr
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
gem install ciphr
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `echo 'hello' | ciphr --hex` | 编码转换 |
| `ciphr 'sha256(secret)'` | 哈希计算 |
| `ciphr 'aes128cbc(key).decrypt(data)'` | AES 解密 |

## 攻击场景 Playbook

### 命令行密码学运算

```bash
echo 'ZGV2' | ciphr --base64 -d
# 渗透中快速编解码
```

## 注意事项

Ruby 密码学 CLI,编码/哈希/加密一体。
