---
name: sourcemapper-js-recover
description: sourcemapper: JS 源码还原挖密钥。信号:web漏洞,注入,下载并还原 JS 源码,本地 map 文件。
---

# sourcemapper

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/denandz/sourcemapper
- 上游 License:BSD-3-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/denandz/sourcemapper@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `sourcemapper -output dir 'https://t.com/static/js/app.js.map'` | 下载并还原 JS 源码 |
| `-output dir app.js.map` | 本地 map 文件 |

## 攻击场景 Playbook

### JS 源码还原挖密钥

```bash
sourcemapper -o src/ 'https://t.com/js/main.bundle.js.map'
# map 文件还原完整源码,grep apiKey/内部端点
```

## 注意事项

从 .map 文件还原原始 JS 源码,前端密钥/内部接口/业务逻辑全暴露,挖逻辑漏洞必备。
