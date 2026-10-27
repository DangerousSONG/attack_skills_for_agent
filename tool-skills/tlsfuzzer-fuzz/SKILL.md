---
name: tlsfuzzer-fuzz
description: tlsfuzzer: TLS 实现 fuzz。信号:密码学攻击,加密破解,协议 fuzz,迭代。
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
