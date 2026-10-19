---
name: bkcrack-zip-plaintext
description: 渗透工具 skill:bkcrack 的安装、参数速查与攻击场景 playbook。当任务涉及 口令与哈希破解 需要调用 bkcrack 时使用。
---

# bkcrack

- 攻击大类:C25 口令与哈希破解
- 上游仓库:https://github.com/kimci86/bkcrack
- 上游 License:Zlib(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/kimci86/bkcrack && cd bkcrack && cmake . && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./bkcrack -L archive.zip` | 查看 ZIP 加密信息 |
| `./bkcrack -C archive.zip -c file.txt -p plain.txt` | 已知明文攻击 |
| `./bkcrack -C archive.zip -c f.txt -k k1 k2 k3` | 用密钥直接解密 |
| `./bkcrack -C a.zip -c f.txt -p plain.txt -d new.zip` | 解密出新 ZIP |

## 攻击场景 Playbook

### ZIP 已知明文攻击

```bash
./bkcrack -C backup.zip -c config.xml -p known_config.xml
# 得到内部密钥后 -d 生成无密码 ZIP
```

## 注意事项

传统 ZipCrypto 已知明文攻击的现代实现,C++ 极快,可秒级恢复加密 ZIP 密钥。
