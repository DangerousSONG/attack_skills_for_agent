---
name: shreder-ssh-brute
description: Shreder: IoT 默认口令批量。信号:密码破解,哈希破解,线程,协议。
---

# Shreder

- 攻击大类:C25 哈希与密码破解
- 上游仓库:https://github.com/EntySec/Shreder
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install shreder
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `shreder 192.168.1.1 -u admin -p pass.txt` | SSH/Telnet 爆破 |
| `-u admin -p p.txt -t 50` | 线程 |
| `-s telnet` | 协议 |

## 攻击场景 Playbook

### IoT 默认口令批量

```bash
shreder 10.0.0.0/24 -u admin -p top100.txt
# 路由器摄像头
```

## 注意事项

EntySec 出品,SSH/Telnet 高速爆破。
