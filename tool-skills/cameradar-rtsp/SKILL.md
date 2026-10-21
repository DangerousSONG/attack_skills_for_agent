---
name: cameradar-rtsp
description: 渗透工具 skill:Cameradar 的安装、参数速查与攻击场景 playbook。当任务涉及 边界设备与VPN攻击 需要调用 Cameradar 时使用。
when-to-use: 渗透工具 skill:Cameradar 的安装、参数速查与攻击场景 playbook。当任务涉及 边界设备与VPN攻击 需要调用 Cameradar 时使用。
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
