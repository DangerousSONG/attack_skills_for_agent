---
name: rfc9000-close-draining-state
description: 审计 QUIC 实现在 closing/draining 关闭状态期间的帧处理义务是否按 RFC 9000 §10.2——closing 状态只可重发 CONNECTION_CLOSE、draining 状态 MUST 不发包不处理，违反即关闭状态机攻击面（关联 CVE-2024-45396 Quicly draining 态处理 ACK 断言失败 QUIC-FUZZ 实证；xquic Stateless Reset/VN 日志 NULL 解引用；nginx QUIC CVE-2024-31079/32760/34161/35200 单会话 worker 崩溃族）
rfc: RFC 9000 §10.2 / §10.2.1 / §10.2.2（Immediate Close、closing 与 draining 状态）/ §10.3（无状态重置，对照）
license: Apache-2.0
---

# RFC 9000 §10.2 关闭与 Draining 状态帧处理义务审计

## 1. 约束条款（原文出处）

RFC 9000 §10.2（原文要点）：
> 立即关闭通过 CONNECTION_CLOSE 帧终止连接；发送方进入 closing 状态并**重发** CONNECTION_CLOSE（以应对丢包），直至收到对端 CONNECTION_CLOSE 或超时进入 draining。

RFC 9000 §10.2.1（closing 状态义务，要点）：
- closing 状态下端点**只可发送 CONNECTION_CLOSE 帧**，不得发送任何其他帧类型；
- closing 状态下收到任何**非** CONNECTION_CLOSE 的帧，MUST 以另一个 CONNECTION_CLOSE 回应（确认对端存活/持续攻击丢包）；
- 收到对端 CONNECTION_CLOSE 或等待超时后进入 draining。

RFC 9000 §10.2.2（draining 状态义务，要点）：
- draining 状态下端点 **MUST NOT 发送任何包**；
- 收到的包被静默丢弃，**不得再处理任何帧**（包括 ACK）；
- draining 期限耗尽后连接状态整体释放。

核心模式一句话：**关闭状态是协议状态机最容易被"已经结束了就随便处理"心态写错的区域——draining 里处理一个 ACK、closing 里回一个 STREAM，就是把半死连接变成崩溃入口。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| CD-1 | 触发服务端进入 draining（先发 CONNECTION_CLOSE 诱使对端关闭再观测，或超时速率探测），随后从对端注入 ACK 帧 | 服务端处理 ACK 并变更状态/崩溃 → 违反 §10.2.2（CVE-2024-45396 同款） |
| CD-2 | closing 状态下持续注入非 CONNECTION_CLOSE 帧（STREAM/ACK/PING），观测服务端回应 | 回非 CC 帧（如 ACK/STREAM）→ 违反 §10.2.1；不回任何 CC → 重发义务缺失（丢包场景对端永远收不到关闭信号） |
| CD-3 | closing 重发节律测量：丢包环境下统计 CC 重发次数与间隔 | 仅发一次不重发 → 关闭信号丢包即幽灵半开连接（义务缺失，非崩溃面但影响状态表堆积） |
| CD-4 | 关闭过程中注入 Stateless Reset 包与 VN 包，观测日志与处理路径 | 触发了 NULL 解引用/日志崩溃 → xquic 同款（QUIC-FUZZ 实证） |
| CD-5 | 并发关闭竞态：双端同时发 CONNECTION_CLOSE（CC 碰撞） | 断言失败/状态机卡死 → 双向关闭处理缺陷 |

判定方法：aioquic 脚本化关闭时序（CC → 状态观测 → 注入帧）；崩溃面配合进程存活探针。

## 3. 攻击面猜想

- **关闭态崩溃 DoS**：CD-1/CD-4 ——draining/closing 代码路径测试覆盖天然薄弱，fuzz 高频命中区（QUIC-Fuzz 6 个目标中 2 个 CVE 出自关闭族）
- **半开连接堆积**：CD-3 ——CC 不重发 + 对端未收到 → 两端状态不一致，服务端状态表被慢速消耗
- **关闭劫持面**：closing 状态下接受并响应非 CC 帧，给"关闭后仍活"的暗道留门

## 4. 关联历史 CVE

| CVE / 实证 | 实现 | 根因 |
|---|---|---|
| **CVE-2024-45396** | Fastly quicly（QUIC-Fuzz 发现） | draining 连接状态下处理 ACK 帧触发断言失败——draining 义务违反的教科书实证 |
| **CVE-2024-45402** | Picotls（QUIC-Fuzz 发现） | 处理意外公钥长度双释放——关闭/握手交叉路径内存错误族 |
| QUIC-Fuzz 附加发现 | XQUIC（Alibaba） | 处理 Stateless Reset 包与 Version Negotiation 日志时 NULL 指针解引用 |
| **CVE-2024-31079 / 32760 / 34161 / 35200** | nginx ngx_http_v3_module（1.25.0–1.25.5、1.26.0） | 单个恶意 QUIC 会话导致 worker 崩溃/内存泄露——H3 会话终结路径缺陷族，关闭态审计必查 |

## 5. 差分验证方法

对照组：quic-go 最新版（draining 严格丢包不处理）、quiche（CC 重发节律符合 §10.2）。
对比字段：CD-1 状态泄漏、CD-2 帧类型白名单、CD-3 重发次数（丢包环境 ≥2 次）、CD-5 双 CC 竞态。
误报排除：closing 状态收到对端 CC 后立即 draining 属合规转移；实现选择在 draining 前保留极短 ACK-only 窗口（争议但可辩护）时标注"策略分歧"而非违规，重点保留 CD-1 崩溃类判定。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`fuzzowski-network-fuzz`（关闭时序帧序列 fuzz）、`grammarinator-gen-fuzz`（CC 碰撞/时序变体生成）
- 工具层（用什么打）：aioquic（脚本化 CONNECTION_CLOSE 时序）、进程存活探针（崩溃判定）、quic-interop-runner（丢包环境 CD-3）
- 命中后动作：崩溃面最小化复现并提取帧序列 → CD-3 测量半开连接堆积速率 → 关闭族缺陷合并进"状态机弱点"证据链
