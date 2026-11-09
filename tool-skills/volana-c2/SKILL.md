---
name: volana-c2
description: "volana: Covert channel C2. Signals: C2, command and control, covert C2, encryption, disguised process."
zh-signals: "volana: 隐蔽信道 C2。信号:c2,命令控制,隐蔽 C2,加密,伪装进程。"
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
