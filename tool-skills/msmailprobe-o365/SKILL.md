---
name: msmailprobe-o365
description: "msmailprobe: O365 environment reconnaissance and spraying. Signals: brute force, password spraying, user enumeration."
zh-signals: "msmailprobe: O365 环境侦察+喷洒。信号:暴力破解,口令喷射,用户枚举。"
---

# msmailprobe

- 攻击大类:C28 暴力破解与口令喷射
- 上游仓库:https://github.com/busterb/msmailprobe
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/busterb/msmailprobe && cd msmailprobe && go build
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./msmailprobe -domain t.com` | O365/Exchange 探测 |
| `-domain d -usernames u.txt` | 用户枚举 |
| `-domain d -spray pass.txt` | 喷洒 |

## 攻击场景 Playbook

### O365 环境侦察+喷洒

```bash
./msmailprobe -domain corp.com -spray passwords.txt
# 判断 IdP 类型+喷洒一体
```

## 注意事项

O365/本地 Exchange 探测+用户枚举+喷洒。
