---
name: sublert-subdomain-mon
description: 渗透工具 skill:Sublert 的安装、参数速查与攻击场景 playbook。当任务涉及 域名与DNS侦察 需要调用 Sublert 时使用。
---

# Sublert

- 攻击大类:C02 域名与DNS侦察
- 上游仓库:https://github.com/yassineaboukir/sublert
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/yassineaboukir/sublert && cd sublert && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 sublert.py -u t.com -l` | 子域监控 |
| `-u domain -l -f 24` | 频率 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 子域变更监控

```bash
python3 sublert.py -u corp.com -l
# 新增子域即时通知,找影子 IT
```

## 注意事项

子域添加监控工具,持续跟踪攻击面变化。
