---
name: whatweb-fingerprint
description: 渗透工具 skill:WhatWeb 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 WhatWeb 时使用。
when-to-use: 渗透工具 skill:WhatWeb 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 WhatWeb 时使用。
---

# WhatWeb

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/urbanadventurer/WhatWeb
- 上游 License:LGPL-2.1(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install whatweb 或 git clone + bundle install
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `whatweb target.com` | 单目标指纹 |
| `-i hosts.txt` | 批量 |
| `-a 3` | 侵略等级(1-4) |
| `--log-json out.json` | JSON 日志 |
| `-v` | 详细 |
| `--follow-redirect=never` | 不重定向 |

## 攻击场景 Playbook

### 批量指纹批扫

```bash
whatweb -i ips.txt -t 50 --log-json=web.json
# 从 json 提取插件命中: jq -r '.plugins | keys[]' web.json
```

## 注意事项

插件式指纹库超 1800 个;侵略等级 3 会触发 WAF,授权边界内用。
