---
name: email2phonenumber
description: email2phonenumber: 邮箱反查手机号。信号:邮箱收集,员工信息,邮箱→手机号,深度模式。
---

# email2phonenumber

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/martinvigo/email2phonenumber
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/martinvigo/email2phonenumber && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python email2phonenumber.py -e victim@gmail.com` | 邮箱→手机号 |
| `-e email -s` | 深度模式 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 邮箱反查手机号

```bash
python email2phonenumber.py -e target@mail.com
# 社工程突破口
```

## 注意事项

OSINT 工具,通过泄露数据反查手机号。
