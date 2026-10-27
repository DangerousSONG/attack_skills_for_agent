---
name: rsatool-rsa-attack
description: rsatool: RSA 参数泄露私钥重建。信号:密码学攻击,加密破解,从 p,q 重建私钥,从 n,d 重建,输出 PEM。
---

# rsatool

- 攻击大类:C49 密码误用与协议分析
- 上游仓库:https://github.com/ius/rsatool
- 上游 License:BSD-2-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/ius/rsatool && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 rsatool.py -p 3233 -q 12377` | 从 p,q 重建私钥 |
| `-n 2419 -d 191` | 从 n,d 重建 |
| `--dumpkey` | 输出 PEM |

## 攻击场景 Playbook

### RSA 参数泄露私钥重建

```bash
python3 rsatool.py -p <素因子> -q <素因子> --dumpkey > key.pem
# 拿到任意因子/私钥指数即重建完整私钥
```

## 注意事项

给定 RSA 任意一组参数(pq/nd/ne/pd 等)重建完整私钥,CTF 与渗透撞见弱 RSA 时用。
