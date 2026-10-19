---
name: windapsearch-ldap-ad
description: 渗透工具 skill:windapsearch 的安装、参数速查与攻击场景 playbook。当任务涉及 AD与LDAP枚举 需要调用 windapsearch 时使用。
---

# windapsearch

- 攻击大类:C29 AD与LDAP枚举
- 上游仓库:https://github.com/ropnop/windapsearch
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/ropnop/windapsearch && cd windapsearch && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python windapsearch.py -d corp.local -u svc -p pass --dc-ip 10.0.0.1 --users` | 枚举用户 |
| `--da` | 仅域管 |
| `--computers` | 计算机 |
| `--gmsa` | gMSA |
| `--psobject` | 自定义 LDAP 查询 |
| `--terms userdescription` | 搜属性关键词 |

## 攻击场景 Playbook

### 自定义 LDAP 查询

```bash
python windapsearch.py -d corp.local -u svc -p pass --dc-ip 10.0.0.1 --psobject "(&(objectCategory=person)(description=*pass*))"
# description 里常写初始密码
```

## 注意事项

ropnop 出品的 LDAP 查询瑞士刀,内置常见查询+支持任意过滤,Python2/3 均有版本。
