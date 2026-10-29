---
name: featherduster-crypto-auto
description: "FeatherDuster cracks weak cryptography in CTF and real-world scenarios. Signals: cryptographic attack, encryption cracking, automatic weak-crypto identification, interactive analysis, module attack."
zh-signals: "FeatherDuster: CTF/真实场景弱加密破解。信号:密码学攻击,加密破解,自动识别并破解弱加密,进入交互分析,选模块攻击。"
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
