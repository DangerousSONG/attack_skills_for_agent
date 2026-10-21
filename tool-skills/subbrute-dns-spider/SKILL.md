---
name: subbrute-dns-spider
description: 渗透工具 skill:SubBrute 的安装、参数速查与攻击场景 playbook。当任务涉及 域名与DNS侦察 需要调用 SubBrute 时使用。
when-to-use: 渗透工具 skill:SubBrute 的安装、参数速查与攻击场景 playbook。当任务涉及 域名与DNS侦察 需要调用 SubBrute 时使用。
---

# SubBrute

- 攻击大类:C02 域名与DNS侦察
- 上游仓库:https://github.com/TheRook/subbrute
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/TheRook/subbrute
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python subbrute.py target.com` | 元查询蜘蛛枚举 |
| `-s subdomains.txt` | 小字典快扫 |
| `-r resolvers.txt` | 自定义 resolver |
| `-t 32` | 线程 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 免字典元查询枚举

```bash
python subbrute.py corp.com
# 利用开放 resolver 做元查询,不依赖大字典也能出子域
```

## 注意事项

特色是 resolver 轮换与元查询,绕开部分 DNS 频率限制;配 massdns 更猛。
