---
name: volana-c2
description: 渗透工具 skill:volana 的安装、参数速查与攻击场景 playbook。当任务涉及 C2框架与远控 需要调用 volana 时使用。
when-to-use: 渗透工具 skill:volana 的安装、参数速查与攻击场景 playbook。当任务涉及 C2框架与远控 需要调用 volana 时使用。
---

# volana

- 攻击大类:C35 C2框架与远控
- 上游仓库:https://github.com/ariary/volana
- 上游 License:Unlicense(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/ariary/volana && cd volana && go build
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./volana -l 10.0.0.5:4444` | 隐蔽 C2 |
| `-e 'cmd'` | 加密 |
| `-p` | 伪装进程 |

## 攻击场景 Playbook

### 隐蔽信道 C2

```bash
./volana -l 443
# 加密+进程伪装
```

## 注意事项

轻量 C2,强调隐蔽。
