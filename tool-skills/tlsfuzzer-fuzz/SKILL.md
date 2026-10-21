---
name: tlsfuzzer-fuzz
description: 渗透工具 skill:tlsfuzzer 的安装、参数速查与攻击场景 playbook。当任务涉及 密码学攻击 需要调用 tlsfuzzer 时使用。
when-to-use: 渗透工具 skill:tlsfuzzer 的安装、参数速查与攻击场景 playbook。当任务涉及 密码学攻击 需要调用 tlsfuzzer 时使用。
---

# tlsfuzzer

- 攻击大类:C49 密码学攻击
- 上游仓库:https://github.com/tomato42/tlsfuzzer
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/tomato42/tlsfuzzer && cd tlsfuzzer && pip install .
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 tests/test_bleichenbacher_timing.py -h t.com -p 443` | Bleichenbacher 时序 |
| `scripts/test-conversation.py -h host` | 协议 fuzz |
| `-n 10` | 迭代 |

## 攻击场景 Playbook

### TLS 实现 fuzz

```bash
python3 tests/test_bleichenbacher_timing.py -h t.com
# padding oracle 时序检测
```

## 注意事项

TLS 协议 fuzz 框架,学术级。
