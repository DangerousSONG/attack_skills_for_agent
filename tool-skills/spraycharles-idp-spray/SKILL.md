---
name: spraycharles-idp-spray
description: 渗透工具 skill:spraycharles 的安装、参数速查与攻击场景 playbook。当任务涉及 暴力破解与口令喷射 需要调用 spraycharles 时使用。
when-to-use: 渗透工具 skill:spraycharles 的安装、参数速查与攻击场景 playbook。当任务涉及 暴力破解与口令喷射 需要调用 spraycharles 时使用。
---

# spraycharles

- 攻击大类:C28 暴力破解与口令喷射
- 上游仓库:https://github.com/Tw1sm/spraycharles
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install spraycharles
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `spraycharles -u users.txt -p pass.txt -a owa -t https://mail.t.com` | 多 IdP 喷洒 |
| `-a adfs` | ADFS |
| `-a okta` | Okta |
| `-t 5` | 线程 |

## 攻击场景 Playbook

### 多平台 IdP 喷洒

```bash
spraycharles -u users.txt -p pass.txt -a adfs -t https://adfs.corp.com
# 13 种 IdP 模板
```

## 注意事项

Tw1sm 出品,支持 13 种身份平台喷洒。
