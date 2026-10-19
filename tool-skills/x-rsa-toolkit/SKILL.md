---
name: x-rsa-toolkit
description: 渗透工具 skill:X-RSA 的安装、参数速查与攻击场景 playbook。当任务涉及 密码学攻击 需要调用 X-RSA 时使用。
---

# X-RSA

- 攻击大类:C49 密码学攻击
- 上游仓库:https://github.com/X-Vector/X-RSA
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/X-Vector/X-RSA && cd X-RSA && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 attack.py -n 2419 -e 65537 -c cipher` | RSA 攻击工具 |
| `-p 61 -q 53` | 分解模式 |
| `-d 2753` | 私钥恢复 |

## 攻击场景 Playbook

### RSA 弱密钥攻击

```bash
python3 attack.py -n $N -e $E -c $C
# 低加密指数/小因子/共模攻击
```

## 注意事项

RSA 攻击合集,CTF 实战向。
