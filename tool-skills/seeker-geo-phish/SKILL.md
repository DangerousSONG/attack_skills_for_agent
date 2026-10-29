---
name: seeker-geo-phish
description: "seeker: precise phishing targeting. Signals: phishing, social engineering, custom phishing page, nearby WiFi phishing template."
zh-signals: "seeker: 精准定位钓鱼。信号:钓鱼,社会工程,手动定制钓鱼页,邻近 WiFi 钓鱼模板。"
---

# seeker

- 攻击大类:C08 钓鱼与社会工程
- 上游仓库:https://github.com/thewhiteh4t/seeker
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/thewhiteh4t/seeker && cd seeker && chmod +x install.sh && ./install.sh
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./seeker.py -t manual` | 手动定制钓鱼页 |
| `-t nearphish` | 邻近 WiFi 钓鱼模板 |
| `-k <key>` | Google Maps API key 配置 |

## 攻击场景 Playbook

### 精准定位钓鱼

```bash
./seeker.py -t manual
# 生成链接发给目标,目标点开后浏览器地理位置授权→回传经纬度
```

## 注意事项

依赖目标授权浏览器定位;务必在授权测试框架内使用。
