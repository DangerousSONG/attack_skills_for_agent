---
name: foresight-prng
description: foresight: 弱 PRNG 预测。信号:密码学攻击,加密破解,LCG 参数恢复。
---

# foresight

- 攻击大类:C49 密码学攻击
- 上游仓库:https://github.com/ALSchwalm/foresight
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install foresight
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python -m foresight gmpredict 12345 67890 11111` | PRNG 预测 |
| `python -m foresight lcg a c m` | LCG 参数恢复 |

## 攻击场景 Playbook

### 弱 PRNG 预测

```bash
python -m foresight mt19937 42
# 恢复梅森旋转种子
```

## 注意事项

PRNG 状态恢复工具,预测弱随机数。
