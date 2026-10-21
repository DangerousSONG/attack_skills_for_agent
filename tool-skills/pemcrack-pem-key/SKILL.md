---
name: pemcrack-pem-key
description: 渗透工具 skill:pemcrack 的安装、参数速查与攻击场景 playbook。当任务涉及 云与身份喷洒 需要调用 pemcrack 时使用。
when-to-use: 渗透工具 skill:pemcrack 的安装、参数速查与攻击场景 playbook。当任务涉及 云与身份喷洒 需要调用 pemcrack 时使用。
---

# pemcrack

- 攻击大类:C28 云与身份喷洒
- 上游仓库:https://github.com/robertdavidgraham/pemcrack
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/robertdavidgraham/pemcrack && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./pemcrack pemfile.pem password.txt` | PEM 私钥口令爆破 |
| `./pemcrack key.pem rockyou.txt` | 字典模式 |

## 攻击场景 Playbook

### 私钥口令爆破(SSH 横向)

```bash
./pemcrack id_rsa rockyou.txt
# 捡到加密私钥先跑一遍,SSH 免密直接通
```

## 注意事项

Robert Graham 出品,加密 PEM 私钥的口令爆破,拿到运维遗留私钥时横向价值大。
