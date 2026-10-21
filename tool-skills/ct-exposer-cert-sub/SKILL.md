---
name: ct-exposer-cert-sub
description: 渗透工具 skill:ct-exposer 的安装、参数速查与攻击场景 playbook。当任务涉及 域名与DNS侦察 需要调用 ct-exposer 时使用。
when-to-use: 渗透工具 skill:ct-exposer 的安装、参数速查与攻击场景 playbook。当任务涉及 域名与DNS侦察 需要调用 ct-exposer 时使用。
---

# ct-exposer

- 攻击大类:C02 域名与DNS侦察
- 上游仓库:https://github.com/chris408/ct-exposer
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/chris408/ct-exposer && cd ct-exposer
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python ct-exposer.py -d t.com` | CT 日志子域发现 |
| `-d domain -o out.txt` | 输出 |

## 攻击场景 Playbook

### CT 日志子域提取

```bash
python ct-exposer.py -d t.com
# 证书透明度历史子域
```

## 注意事项

证书透明度子域发现工具。
