---
name: creddump-sam-extract
description: 渗透工具 skill:creddump 的安装、参数速查与攻击场景 playbook。当任务涉及 口令与哈希破解 需要调用 creddump 时使用。
when-to-use: 渗透工具 skill:creddump 的安装、参数速查与攻击场景 playbook。当任务涉及 口令与哈希破解 需要调用 creddump 时使用。
---

# creddump

- 攻击大类:C25 口令与哈希破解
- 上游仓库:https://github.com/moyix/creddump
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/moyix/creddump
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python2 pwdump.py SYSTEM SAM` | 从注册表 hive 提取 LM/NT 哈希 |
| `python2 cachedump.py SYSTEM SECURITY` | 提取缓存域凭证(mscash) |
| `python2 lsadump.py SYSTEM SECURITY` | 提取 LSA 密钥 |

## 攻击场景 Playbook

### 离线 SAM 哈希提取

```bash
python2 pwdump.py /mnt/win/Windows/System32/config/SYSTEM /mnt/win/.../SAM
# 得哈希后接 hashcat -m 1000
```

## 注意事项

经典的离线注册表解析工具,Python2。同类现代替代 secretsdump(现有)无法离线时用它。
