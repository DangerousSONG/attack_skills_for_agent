---
name: drozer-android
description: 渗透工具 skill:Drozer 的安装、参数速查与攻击场景 playbook。当任务涉及 移动端攻击 需要调用 Drozer 时使用。
---

# Drozer

- 攻击大类:C43 移动端攻击
- 上游仓库:https://github.com/FSecureLABS/drozer
- 上游 License:NOASSERTION(需人工)(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install drozer 或 release .deb
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `drozer console connect` | 连接 agent |
| `run app.package.list -f target` | 列包 |
| `run app.package.attacksurface com.target` | 攻击面分析 |
| `run app.activity.info -a pkg` | 导出 Activity |
| `run app.provider.query uri` | 读 ContentProvider |
| `run shell.start` | 设备 shell |

## 攻击场景 Playbook

### Android 组件暴露审计

```bash
run app.package.attacksurface com.target.app
run app.activity.start --component pkg com.pkg.DebugActivity  # 直接拉起隐藏调试界面
run scanner.provider.injection -a pkg  # SQL 注入检测
```

## 注意事项

Android 安全测试标杆;需目标 app 装 agent 或 USB 调试授权环境。
