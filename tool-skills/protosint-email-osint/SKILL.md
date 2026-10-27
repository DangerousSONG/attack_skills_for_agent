---
name: protosint-email-osint
description: ProtOSINT: 邮箱泄露情报。信号:邮箱收集,员工信息,手机号社工库查询,域名关联邮箱探测。
---

# ProtOSINT

- 攻击大类:C03 OSINT情报收集
- 上游仓库:https://github.com/pixelbubble/ProtOSINT
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/pixelbubble/ProtOSINT && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 protOSINT.py -m mail -e target@mail.com` | 邮箱多源 OSINT(HIBP/粘贴站) |
| `-m phone -p +1234` | 手机号社工库查询 |
| `-m domain -d t.com` | 域名关联邮箱探测 |
| `-o report.txt` | 输出 |

## 攻击场景 Playbook

### 邮箱泄露情报

```bash
python3 protOSINT.py -m mail -e ceo@corp.com
# 历史泄露密码/数据外泄事件,判断撞库与钓鱼素材
```

## 注意事项

邮箱/手机号/域名的泄露数据聚合查询,免 API key,适合社工前期情报。
