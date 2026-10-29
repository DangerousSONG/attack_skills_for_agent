---
name: whatportis-service
description: "whatportis: Non-standard port identification. Signals: port scan, nmap, port service query, service reverse lookup, fuzzy."
zh-signals: "whatportis: 非标准端口识别。信号:端口扫描,nmap,端口服务查询,服务反查,模糊。"
---

# whatportis

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/ncrocfer/whatportis
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install whatportis
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `whatportis 3306` | 端口服务查询 |
| `whatportis mysql` | 服务反查 |
| `--like` | 模糊 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 非标准端口识别

```bash
whatportis 8443
# 指纹识别辅助
```

## 注意事项

端口-服务映射查询,IOC 分析辅助。
