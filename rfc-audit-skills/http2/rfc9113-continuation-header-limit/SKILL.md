---
name: rfc9113-continuation-header-limit
description: 审计 HTTP/2 实现 CONTINUATION 帧与头块大小限制执行是否安全——超限头块为生成 413 而无界缓冲、END_HEADERS 永不置位即内存耗尽 DoS（关联 CVE-2024-27316 Apache httpd 2.4.17-2.4.58 nghttp2 缓冲内存耗尽；CERT VU#421644 帧类；CVE-2024-24549 Tomcat、CVE-2024-30255 Envoy 同族变体）
rfc: RFC 9113 §6.10（HEADERS/CONTINUATION 序列）/ §6.5.2（SETTINGS_MAX_HEADER_LIST_SIZE）/ RFC 7540 §10.5.1（头块上限）
license: Apache-2.0
---

# RFC 9113 §6.10 CONTINUATION 帧与头块限长执行审计

## 1. 约束条款（原文出处）

RFC 9113 §6.5.2（要点）：
> SETTINGS_MAX_HEADER_LIST_SIZE（0x06）声明端点愿意接受的**未压缩**头列表大小（每个字段名+值 octet 数 + 每字段 32 octet 开销）；超限消息为 **malformed**，应被拒。

RFC 9113 §6.10（要点）：
> 头块由 HEADERS + 任意数量 CONTINUATION 帧组成，序列中 END_HEADERS 未置位前不得出现其他帧；CONTINUATION 只能跟在头块中间帧之后。

RFC 7540 §10.5.1（要点）：
> 中间件与端点 MUST 能对头块大小施加上限——实现可选用低于对端声明的值执行，但超限后的处理路径必须**有界**。

核心模式一句话：**这个 CVE 类的根因不是"没有限制"，而是"超过限制后的错误处理路径是无界的"——为了给客户端一个体面的 413，先把攻击者的无限流缓冲下来。好心成了放大器。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| CT-1 | 建立连接后发送 HEADERS（不置 END_HEADERS），随后无限续发 CONTINUATION（永不置 END_HEADERS），观测服务端 RSS | 内存持续增长无硬顶 → CVE-2024-27316 同款（413 缓冲路径无界） |
| CT-2 | 头块超过 SETTINGS_MAX_HEADER_LIST_SIZE 后继续发送 CONTINUATION | 服务端未在超限点即断开/重置，而是继续接收缓冲 → 执行路径有界性违规 |
| CT-3 | CONTINUATION 序列中间插入非 CONTINUATION 帧（PING/DATA） | 未按协议错误断开 → 帧序列校验缺失 |
| CT-4 | 多流交错构造：流 A 头块未完结时发流 B 的 HEADERS | 未拒绝 → 实现允许头块交叉，状态面扩大 |
| CT-5 | 头块完结后尾随额外 CONTINUATION | 未拒绝 → 序列终止校验缺失 |

判定方法：自定义 H2 客户端（h2 库底层帧控制）；RSS 采样 + 413 响应到达时间差测量。

## 3. 攻击面猜想

- **单连接内存耗尽 DoS**：CT-1 ——发现者评估：比 Rapid Reset 更省资源，单 TCP 连接即可打崩部分实现
- **头解析状态面扩大**：CT-3/CT-4 ——交错序列下解码器状态机混乱 → 崩溃/UAF 族
- **头块边界混淆**：CT-5 ——多算/少算头块边界为解析分裂留缝

## 4. 关联历史 CVE

| CVE | 实现 | 根因 |
|---|---|---|
| **CVE-2024-27316** | Apache httpd 2.4.17–2.4.58（nghttp2，CVSS 7.5） | 超限头为生成 413 被临时缓冲，客户端不停则缓冲无界 → 内存耗尽。修复：解析错误超阈值即终止（httpd commit 0d73970ec161） |
| **CVE-2024-24549** | Apache Tomcat | 请求超头限制时流未在处理完所有头前 reset——同族变体 |
| **CVE-2024-30255** | Envoy（nghttp2 集成面） | CONTINUATION 处理资源消耗无界，同族 |
| CERT VU#421644 | 帧类披露（Bartek Nowotarski，2024-04） | CONTINUATION Flood 作为**帧类**披露：不限于 Apache，是 H2 实现通用弱点 |

## 5. 差分验证方法

对照组：httpd ≥2.4.59（修复版：错误计数阈值终止）、nghttp2 ≥1.61（若已含帧数上限逻辑）。
对比字段：CT-1 RSS 封顶值、CT-2 超限断开时点（应在超限瞬间而非缓冲后）、CT-3/CT-4/CT-5 拒绝率。
误报排除：服务端在收到 N 帧后正常断开且 RSS 有界属合规策略差异；只判定"无界缓冲"与"序列校验缺失"。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`slowhttptest-dos`（单连接慢速头块流模式）、`fuzzowski-network-fuzz`（CONTINUATION 序列语法 fuzz）
- 工具层（用什么打）：Python h2 库（帧级控制）、RSS 采样脚本、CVE-2024-27316 PoC 参考实现
- 命中后动作：测量单连接内存注入速率 → CT-1 最小化复现帧序列 → 评估多连接并发放大（内存耗尽斜率 × 连接数）
