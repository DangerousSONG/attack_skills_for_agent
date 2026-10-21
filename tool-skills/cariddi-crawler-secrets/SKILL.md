---
name: cariddi-crawler-secrets
description: 渗透工具 skill:cariddi 的安装、参数速查与攻击场景 playbook。当任务涉及 API与业务逻辑攻击 需要调用 cariddi 时使用。
when-to-use: 渗透工具 skill:cariddi 的安装、参数速查与攻击场景 playbook。当任务涉及 API与业务逻辑攻击 需要调用 cariddi 时使用。
---

# cariddi

- 攻击大类:C10 API与业务逻辑攻击
- 上游仓库:https://github.com/edoardottt/cariddi
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/edoardottt/cariddi@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `cat hosts.txt | cariddi` | 爬站+秘密提取 |
| `-s` | 只爬不扫描 |
| `-e php,jsp` | 扩展名过滤 |
| `-d 3` | 爬深 |
| `-i ignore.txt` | 忽略路径 |
| `-headers` | 输出头 |
| `-secrets` | 开秘密扫描 |

## 攻击场景 Playbook

### 源码级秘密收割

```bash
echo https://target.com | cariddi -s -d 3 | tee urls.txt
cat urls.txt | cariddi -secrets -headers  # API key/令牌/内部地址提取
```

## 注意事项

Go 写的快爬虫,秘密提取正则覆盖 40+ 模式;管道友好。
