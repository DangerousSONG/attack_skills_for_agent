---
name: featherduster-crypto-auto
description: 渗透工具 skill:FeatherDuster 的安装、参数速查与攻击场景 playbook。当任务涉及 密码误用与协议分析 需要调用 FeatherDuster 时使用。
when-to-use: 渗透工具 skill:FeatherDuster 的安装、参数速查与攻击场景 playbook。当任务涉及 密码误用与协议分析 需要调用 FeatherDuster 时使用。
---

# FeatherDuster

- 攻击大类:C49 密码误用与协议分析
- 上游仓库:https://github.com/nccgroup/featherduster
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/nccgroup/featherduster && cd featherduster && pip install .
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 featherduster.py secrets.txt` | 自动识别并破解弱加密 |
| `analyze` | 进入交互分析 |
| `use rsa_wiener` | 选模块攻击 |
| `run` | 执行 |

## 攻击场景 Playbook

### CTF/真实场景弱加密破解

```bash
python3 featherduster.py leaked_ciphertext.txt
# 自动检测 XOR/重复密钥/RSA 小公钥/单向截断等并给出明文
```

## 注意事项

NCC 出品,自动多路识别弱加密并攻击(XOR/维吉尼亚/RSA 常见误用),密码误用审计利器。
