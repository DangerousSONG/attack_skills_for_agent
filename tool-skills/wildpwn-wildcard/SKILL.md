---
name: wildpwn-wildcard
description: 渗透工具 skill:wildpwn 的安装、参数速查与攻击场景 playbook。当任务涉及 Linux本地提权 需要调用 wildpwn 时使用。
---

# wildpwn

- 攻击大类:C16 Linux本地提权
- 上游仓库:https://github.com/localh0t/wildpwn
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/localh0t/wildpwn
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python wildpwn.py combined /var/www` | 通配符注入 |
| `--file file` | 指定 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### tar/chmod 通配符提权

```bash
python wildpwn.py tar /backup
# checkpoint 提权
```

## 注意事项

通配符注入提权工具。
