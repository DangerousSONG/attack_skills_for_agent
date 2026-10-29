---
name: postenum-linux-audit
description: "Quick Linux foothold assessment. Signals: red team, methodology, basic system info, container/virtualization detection, network info."
zh-signals: "postenum: Linux 立足点快速摸底。信号:红队,方法论,基础系统信息,容器/虚拟化检测,网络信息。"
---

# postenum

- 攻击大类:C50 痕迹清理与反取证
- 上游仓库:https://github.com/mbahadou/postenum
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/mbahadou/postenum
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `bash postenum.sh -s` | 基础系统信息 |
| `bash postenum.sh -c` | 容器/虚拟化检测 |
| `bash postenum.sh -n` | 网络信息 |
| `bash postenum.sh -a` | 全量 |

## 攻击场景 Playbook

### Linux 立足点快速摸底

```bash
bash postenum.sh -a | tee enum.txt
# 内核版本/ Suid/cron/docker/云元数据一把梭,找提权路径
```

## 注意事项

Linux 提权枚举脚本,输出按 MITRE ATT&CK 分类,比 LinPEAS 更轻量。
