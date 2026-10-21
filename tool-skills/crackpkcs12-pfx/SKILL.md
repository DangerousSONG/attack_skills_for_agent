---
name: crackpkcs12-pfx
description: 渗透工具 skill:crackpkcs12 的安装、参数速查与攻击场景 playbook。当任务涉及 哈希与密码破解 需要调用 crackpkcs12 时使用。
when-to-use: 渗透工具 skill:crackpkcs12 的安装、参数速查与攻击场景 playbook。当任务涉及 哈希与密码破解 需要调用 crackpkcs12 时使用。
---

# crackpkcs12

- 攻击大类:C25 哈希与密码破解
- 上游仓库:https://github.com/crackpkcs12/crackpkcs12
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/crackpkcs12/crackpkcs12 && cd crackpkcs12 && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./crackpkcs12 -d wordlist.txt cert.pfx` | PFX 口令爆破 |
| `-d w.txt -f pfx -v` | 详细 |

## 攻击场景 Playbook

### PFX 证书口令爆破

```bash
./crackpkcs12 -d rockyou.txt backup.pfx
# 得私钥签名任意
```

## 注意事项

PKCS#12 证书口令爆破工具。
