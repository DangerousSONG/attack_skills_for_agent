---
name: domained-multi-enum
description: 渗透工具 skill:Domained 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 Domained 时使用。
---

# Domained

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/TypeError/domained
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/TypeError/domained && cd domained && python domained.py -i target.com -p
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python domained.py -i target.com -p` | 被动+主动子域 |
| `-b` | 仅爆破 |
| `-a` | 仅主动 |

## 攻击场景 Playbook

### 多工具编排子域收集

```bash
python domained.py -i corp.com -p  # 调 sublist3r/enumall/subfinder/amass 汇总
```

## 注意事项

一键编排多个子域工具去重汇总;省得自己写管道。
