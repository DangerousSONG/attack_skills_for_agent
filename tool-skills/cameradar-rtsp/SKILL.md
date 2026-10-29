---
name: cameradar-rtsp
description: "Cameradar: Takes over surveillance cameras via weak passwords. Signals: VPN vulnerability, firewall, RTSP port scanning, specified ports, default credential dictionary."
zh-signals: "Cameradar: 监控摄像头弱口令接管。信号:vpn漏洞,防火墙,扫描 RTSP 端口,指定端口,默认凭据字典。"
---

# Cameradar

- 攻击大类:C11 边界设备与VPN攻击
- 上游仓库:https://github.com/Ullaakut/cameradar
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
docker run -t ullaakut/cameradar -t 192.168.0.0/24 或 go install
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `-t target / CIDR` | 扫描 RTSP 端口 |
| `-p 554,8554` | 指定端口 |
| `-r /dictionaries/credentials.json` | 默认凭据字典 |
| `-s` | 禁截图 |
| `-o /tmp/out` | 输出 |

## 攻击场景 Playbook

### 监控摄像头弱口令接管

```bash
cameradar -t 10.0.0.0/24
# 自动尝试 admin/admin 等常见 RTSP 凭据并验证流地址 rtsp://ip:554/stream
```

## 注意事项

默认内置 133 条常见摄像头凭据;拿到 rtsp 流后可 ffmpeg 拉流取证。
