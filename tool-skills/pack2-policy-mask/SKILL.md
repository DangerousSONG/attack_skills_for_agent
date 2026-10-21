---
name: pack2-policy-mask
description: 渗透工具 skill:Pack2 的安装、参数速查与攻击场景 playbook。当任务涉及 口令与哈希破解 需要调用 Pack2 时使用。
when-to-use: 渗透工具 skill:Pack2 的安装、参数速查与攻击场景 playbook。当任务涉及 口令与哈希破解 需要调用 Pack2 时使用。
---

# Pack2

- 攻击大类:C25 口令与哈希破解
- 上游仓库:https://github.com/hops/pack2
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/hops/pack2 && cd pack2 && go build -o pack2
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./pack2 policy --length 8-12 --charsets luds` | 生成合规掩码(公司口令策略) |
| `./pack2 stats -i rockyou.txt` | 统计字典特征 |
| `./pack2 analyze -i hashes.txt` | 分析已破哈希 |

## 攻击场景 Playbook

### 按口令策略生成掩码

```bash
./pack2 policy -l 8-12 --charsets ulds --output masks.txt
# 把公司 '大写+小写+数字+特殊 8位+' 策略转成 hashcat 掩码
```

## 注意事项

hashcat 团队新工具,将企业口令策略转成高效掩码,策略合规破解提速显著。
