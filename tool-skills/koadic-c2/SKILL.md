---
name: koadic-c2
description: 渗透工具 skill:Koadic 的安装、参数速查与攻击场景 playbook。当任务涉及 C2框架与远控 需要调用 Koadic 时使用。
---

# Koadic

- 攻击大类:C35 C2框架与远控
- 上游仓库:https://github.com/zerosum0x0/koadic
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/zerosum0x0/koadic && cd koadic && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 koadic` | C2 控制台 |
| `use stager/js/implant` | 载荷选择 |
| `set SRVHOST 10.0.0.5` | 监听 |
| `run` | 执行 |

## 攻击场景 Playbook

### JScript/VBScript C2

```bash
python3 koadic && use stager/js/wmic
# COM 无文件攻击
```

## 注意事项

zerosum0x0 出品,Windows 无文件 C2。
