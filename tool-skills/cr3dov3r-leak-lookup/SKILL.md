---
name: cr3dov3r-leak-lookup
description: 渗透工具 skill:Cr3dOv3r 的安装、参数速查与攻击场景 playbook。当任务涉及 邮箱与人员OSINT 需要调用 Cr3dOv3r 时使用。
when-to-use: 渗透工具 skill:Cr3dOv3r 的安装、参数速查与攻击场景 playbook。当任务涉及 邮箱与人员OSINT 需要调用 Cr3dOv3r 时使用。
---

# Cr3dOv3r

- 攻击大类:C03 邮箱与人员OSINT
- 上游仓库:https://github.com/D4Vinci/Cr3dOv3r
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/D4Vinci/Cr3dOv3r && cd Cr3dOv3r && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python Cr3dOv3r.py victim@email.com` | breach 库+凭据复用检查 |
| `-q` | 静默 |
| `-p` | 只查明文密码库 |
| `-np` | 不测试凭据复用 |

## 攻击场景 Playbook

### 泄露凭据收集+复用验证

```bash
python Cr3dOv3r.py admin@corp.com
# 输出 HaveIBeenPwned 泄露记录+明文密码,并尝试在各平台复用登录
```

## 注意事项

把'查泄露'和'测复用'串成一条;项目更新放缓,结果需人工复核。
