---
name: deepce-container-escape
description: "deepce: Docker enumeration and escape paths. Signals: cloud command execution, container escape, full container enumeration, automatic escape attempts, run all escape checks."
zh-signals: "deepce: Docker 内枚举+逃逸路径。信号:云命令执行,容器逃逸,容器内全面枚举,自动尝试逃逸,跑所有逃逸检测。"
---

# deepce

- 攻击大类:C14 云与容器执行
- 上游仓库:https://github.com/stealthcopter/deepce
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
curl -s https://raw.githubusercontent.com/stealthcopter/deepce/main/deepce.sh -o deepce.sh && chmod +x deepce.sh
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./deepce.sh` | 容器内全面枚举 |
| `-e` | 自动尝试逃逸 |
| `--exploit` | 跑所有逃逸检测 |
| `--no-enumeration` | 跳过枚举 |
| `--cve` | 输出 CVE 命中 |

## 攻击场景 Playbook

### Docker 内枚举+逃逸路径

```bash
./deepce.sh  # 查: socket挂载/特权模式/危险capability/可写宿主机路径
./deepce.sh -e  # 对命中项自动逃逸尝试
```

## 注意事项

对标 LinEnum 的容器版;发现 docker.sock 挂载即可挂载宿主机根目录写 crontab。
