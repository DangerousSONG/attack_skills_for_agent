---
name: trape-osint-track
description: 渗透工具 skill:trape 的安装、参数速查与攻击场景 playbook。当任务涉及 邮箱与人员OSINT 需要调用 trape 时使用。
when-to-use: 渗透工具 skill:trape 的安装、参数速查与攻击场景 playbook。当任务涉及 邮箱与人员OSINT 需要调用 trape 时使用。
---

# trape

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/jofpin/trape
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/jofpin/trape && cd trape && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python trape.py -u https://target.com -p 8080` | 对目标站点做访问者追踪 |
| `-l` | 本地演示模式 |
| `--custom` | 自定义注入页面 |

## 攻击场景 Playbook

### 目标访问行为追踪

```bash
python trape.py -u https://news.site -p 8080
# 目标点开你构造的链接后: IP/UA/地理位置/在线时长回传控制面板
```

## 注意事项

项目较老(2018-2020),新式浏览器 SameSite Cookie 策略下能力受限;轻量场景可用。
