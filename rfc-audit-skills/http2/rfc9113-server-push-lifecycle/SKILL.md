---
name: rfc9113-server-push-lifecycle
description: 审计 HTTP/2 服务端推送（PUSH_PROMISE/reserved 流）生命周期实现——推送开启即攻击面放大器：Cache-Digest 头触发推送时崩溃（CVE-2020-9490 Apache httpd 2.4.20-2.4.43，CVSS 7.5，H2Push off 缓解）；推送方法访问控制失效（CVE-2023-30631 Apache Traffic Server push_method_enabled 配置失效，CVSS 7.5）；http4s Ember 推送帧 DoS（CVE-2026-69203，缓解靠代理剥离 PUSH_PROMISE）；RFC 9113 §6.6/§8.4 要求客户端可拒绝推送、服务端可宣告 ENABLE_PUSH=0，但 reserved 流状态机的实现义务分散且历史上反复出事
rfc: RFC 9113 §6.6（PUSH_PROMISE）/ §8.4（Server Push）/ §5.1（reserved 流状态）
license: Apache-2.0
---

# RFC 9113 §6.6/§8.4 服务端推送生命周期审计

## 1. 约束条款（原文出处）

RFC 9113 §8.4（要点）：
> 服务端**不得**推送任何客户端未请求过的资源；客户端可通过 `SETTINGS_ENABLE_PUSH=0` 宣告不接受推送并**必须**将其作为连接错误处理违规推送；PUSH_PROMISE 承诺的流进入 reserved 状态，后续只能经 HEADERS/RST_STREAM 收敛。

核心模式一句话：**推送是把"服务端主动建流"这个特权交给应用配置的开关——历史上它反复成为崩溃源（Cache-Digest）、访问控制失效源（推送方法鉴权缺失）和 DoS 源（承诺流不收敛）。RFC 给了客户端拒绝机制（ENABLE_PUSH=0 + 违规即连接错误），审计先看"你默认开没开"，再看"开了之后 reserved 流状态机和推送载荷校验有没有跟上"。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| SP-1 | 客户端发 `SETTINGS_ENABLE_PUSH=0` 后仍收到 PUSH_PROMISE | 未按连接错误（PROTOCOL_ERROR）断开 → §8.4 拒绝机制失效 |
| SP-2 | 构造畸形 Cache-Digest 值（gzip 无效负载/超大声明）后诱导服务端推送 | 服务端在推送路径崩溃 → CVE-2020-9490 同款 |
| SP-3 | PUSH_PROMISE 出现在客户端宣告禁推的连接上 | 未拒绝/未断开 → 与 SP-1 互补的服务端义务缺失 |
| SP-4 | PUSH_PROMISE 的 promised stream ID 为偶数（客户端发起方向）或已被占用 | 未按连接错误处理 → §6.6 流 ID 校验缺失 |
| SP-5 | reserved 流长期不收敛（不发 HEADERS 也不 RST） | 无超时清理 → 承诺流驻留占用流表（与 H3 侧 skill 同模式） |
| SP-6 | 通过 PUSH 方法（RFC 8297 前身的扩展语义）请求 + 推送方法访问控制 | 推送路径绕过常规方法鉴权 → CVE-2023-30631 同类 |

判定方法：h2 客户端宣告 ENABLE_PUSH=0 后观测推送行为；构造 Cache-Digest 变体诱导推送；统计 reserved 流驻留时长。

## 3. 攻击面猜想

- **远程崩溃 DoS**：SP-2 ——推送路径是覆盖率低的历史崩溃高发区（Cache-Digest 解析、gzip 处理）
- **访问控制绕过**：SP-6 ——推送方法若绕过常规 HTTP 方法鉴权矩阵，等价于隐藏的攻击入口
- **流表驻留**：SP-5 ——不收敛的 reserved 流与并发流上限计数交互，可冻结并发配额

## 4. 关联历史 CVE

| CVE | 实现 | 根因 |
|---|---|---|
| **CVE-2020-9490** | Apache httpd 2.4.20–2.4.43（mod_http2） | 特制 Cache-Digest 头值 → 服务端执行 HTTP/2 PUSH 时崩溃；`H2Push off` 可缓解；CVSS 7.5 |
| **CVE-2023-30631** | Apache Traffic Server 8.0.0–9.2.0 | `proxy.config.http.push_method_enabled` 配置不生效（输入校验缺陷），推送方法访问控制失效；CVSS 7.5 |
| **CVE-2026-69203** | http4s Ember Server | 推送帧相关 DoS；官方缓解为代理层剥离 PUSH_PROMISE 帧；修复 0.23.35 |
| 交叉引用 | H3 侧 `rfc9114-server-push-frame-rejection` | 同一攻击模式在 QUIC 栈的平行审计（服务端必须接受客户端对推送的拒绝） |

## 5. 差分验证方法

对照组：ENABLE_PUSH=0 后绝无任何 PUSH_PROMISE 的 nginx/Envoy 现代版本。
对比字段：SP-1/SP-3 错误处置、SP-2 推送路径健壮性、SP-5 reserved 流超时。
误报排除：中间代理解释并终结推送（转发为常规 200 响应）→ 判定通过；推送关闭但实现保留了预留代码路径未被触发 → 仅记录暴露面不记违规。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`fuzzowski-network-fuzz`（PUSH_PROMISE/Cache-Digest 变异）、`dharma-grammar-fuzz`（推送帧序列生成）
- 工具层（用什么打）：Python h2（ENABLE_PUSH=0 宣告 + 推送观测）、内存/崩溃采样
- 命中后动作：SP-1 确认 → 验证推送内容是否绕过认证资源 → 输出"禁推宣告失效"证据链；SP-2 确认 → 最小崩溃负载归档
