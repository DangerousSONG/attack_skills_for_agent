---
name: nullinux-smb-enum
description: Nullinux: Linux 上 SMB 枚举一把梭。信号:资产测绘,指纹识别,SMB/RPC 全枚举,共享枚举,用户枚举。
---

# Nullinux

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/m8r0wn/nullinux
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/m8r0wn/nullinux && cd nullinux && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python nullinux.py 10.0.0.5` | SMB/RPC 全枚举 |
| `-shares` | 共享枚举 |
| `-users` | 用户枚举 |
| `-quick` | 快速模式 |

## 攻击场景 Playbook

### Linux 上 SMB 枚举一把梭

```bash
python nullinux.py 10.0.0.0/24 -users -shares  # 域用户/共享/组/RID 全出
```

## 注意事项

enum4linux 的现代化 Python 版;输出规整适合脚本消费。
