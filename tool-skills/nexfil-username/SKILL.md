---
name: nexfil-username
description: "nexfil: Cross-platform username tracking. Signals: email collection, employee information, username internet-wide existence, concurrency."
zh-signals: "nexfil: 用户名跨平台追踪。信号:邮箱收集,员工信息,用户名全网存在性,并发。"
---

# nexfil

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/thewhiteh4t/nexfil
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/thewhiteh4t/nexfil && cd nexfil && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 nexfil.py -u username` | 用户名全网存在性 |
| `-u user -c 50` | 并发 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 用户名跨平台追踪

```bash
python3 nexfil.py -u targetuser
# 350+ 平台存在性
```

## 注意事项

whiteh4t 出品,用户名 OSINT。
