---
name: syborg-recursive-sub
description: 渗透工具 skill:Syborg 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 Syborg 时使用。
---

# Syborg

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/MustafaTanguner/Syborg
- 上游 License:NOASSERTION(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/MustafaTanguner/Syborg
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python syborg.py corp.com -w wordlist.txt` | 递归子域枚举 |
| `-r resolvers.txt` | resolver |

## 攻击场景 Playbook

### 递归+通配符规避爆破

```bash
python syborg.py corp.com -w all.txt  # 递归爆破 dev.x.corp.com 深层子域
```

## 注意事项

递归枚举模式 + Sublist3r 式多源融合。
