---
name: wildpwn-wildcard
description: wildpwn: tar/chmod 通配符提权。信号:linux提权,suid,通配符注入。
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
