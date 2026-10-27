---
name: enum4linux-ng
description: enum4linux-ng: 匿名/凭据双模式域信息收割、工作组环境快速摸底。信号:内网枚举,网络发现,所有模块,带凭据。
---

# enum4linux-ng

- 攻击大类:C29 内网发现与枚举
- 上游仓库:https://github.com/cddmp/enum4linux-ng
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/cddmp/enum4linux-ng && cd enum4linux-ng && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./enum4linux-ng.py 10.0.0.5` | 全量 SMB/RPC/LDAP 枚举 |
| `-A` | 所有模块 |
| `-u user -p pass` | 带凭据 |
| `-R/-S/-U` | 分别: 用户/共享/策略 |
| `-w workgroup` | 指定工作组 |
| `-oJ out.json` | JSON 输出 |
| `-p 139,445` | 端口 |

## 攻击场景 Playbook

### 匿名/凭据双模式域信息收割

```bash
./enum4linux-ng.py 10.0.0.5 -oJ enum.json
# 输出: 域SID/用户表/共享表/密码策略/OS/打印机,直接喂密码喷洒
```

### 工作组环境快速摸底

```bash
./enum4linux-ng.py 192.168.1.10 -w WORKGROUP
```

## 注意事项

enum4linux 的 Python 重写版,输出 JSON 适合 Agent 管道解析;LDAP 模块需域控可达。
