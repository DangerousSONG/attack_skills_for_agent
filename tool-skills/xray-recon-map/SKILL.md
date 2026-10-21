---
name: xray-recon-map
description: 渗透工具 skill:XRay 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 XRay 时使用。
when-to-use: 渗透工具 skill:XRay 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 XRay 时使用。
---

# XRay

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/evilsocket/xray
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/evilsocket/xray@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `xray -shodan-key X -domain corp.com` | Shodan 驱动测绘 |
| `-domain corp.com -wordlist words.txt` | 字典模式 |

## 攻击场景 Playbook

### Shodan 数据驱动的资产图谱

```bash
xray -shodan-key $KEY -domain corp.com -o report
# 自动: Shodan 搜目标→端口/服务/漏洞关联→HTML 图谱
```

## 注意事项

evilsocket 出品;用 Shodan 数据替代主动扫描,隐蔽性极好。
