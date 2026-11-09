---
name: rfc9114-grease-reserved-frames
description: 审计 HTTP/3 实现对 GREASE/保留帧类型、保留 SETTINGS 标识、未知单向流类型的容忍义务是否按 RFC 9114 §9/§7.2.8——未知帧必须按长度跳过不得拒绝，H2 保留帧 0x02/0x06/0x08/0x09 必须炸连接不得当 GREASE 跳过；拒绝 GREASE 即前向兼容断点（关联实证：aioquic <1.6 流尾 GREASE 帧导致流数据丢失；保留帧与 H2 走私帧边界混淆即走私暗道面）
rfc: RFC 9114 §9（Extensions/未知帧容忍）/ §7.2.8（保留帧类型 0x1f·N+0x21 与 H2 保留帧）/ §7.2.4.1（SETTINGS 未知标识容忍）/ §6.2（未知单向流类型）/ RFC 8701（QUIC 传输层 GREASE，对照：QUIC 层无可忽略帧类型 RFC 9000 §12.4）
license: Apache-2.0
---

# RFC 9114 §9/§7.2.8 GREASE 与保留帧容忍义务审计

## 1. 约束条款（原文出处）

RFC 9114 §9 / §7.2.8（要点，两处互证）：
> Unknown frame types (including reserved GREASE types 0x1f * N + 0x21) MUST be ignored by length skipping——reserved frame types exist precisely to catch implementations that do not.

RFC 9114 §7.2.8（H2 保留帧边界，原文要点）：
> 帧类型 0x02（PRIORITY）、0x06（PING）、0x08（WINDOW_UPDATE）、0x09（CONTINUATION）在 H3 被永久保留，收到 MUST 视为连接错误 H3_FRAME_UNEXPECTED——**它们是"已知被禁止"而非"未知"，把它们当 GREASE 跳过 = 让走私上 H3 的 H2 帧被静默吞掉**。

RFC 9114 §7.2.4.1（SETTINGS 容忍，要点）：
> 未知 / 保留 SETTINGS 标识 MUST 被忽略（grease tolerance），不得触发 SETTINGS_ERROR。

RFC 9114 §6.2（未知单向流类型，要点）：
> 未识别的单向流类型 MUST 被忽略（读取并丢弃），不得关闭连接。

RFC 9000 §12.4（对照基准）：
> QUIC 传输层不保留任何"可忽略帧类型"——传输层收到未知帧是协议错误；忽略义务是 H3 层的。审计时不得把两层的容忍语义混为一谈。

核心模式一句话：**GREASE 是协议给自己埋的探雷器——对 GREASE 报错就是对未来扩展断路的预告；而把 H2 保留帧当未知帧容忍，则是在"未知"和"已知禁止"的边界上给走私留暗道。容忍义务的双向精确性是这个条款的考点。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| GR-1 | 在请求流/控制流上发送保留 GREASE 帧（0x21、0x40、0x1f·N+0x21 族）+ 合法长度 | 连接被关闭/报错 → 违反 §9（前向兼容断点）；静默跳过 → 合规 |
| GR-2 | 发送 H2 保留帧 0x02/0x06/0x08/0x09 于任何流 | 被当作未知帧跳过 → 违反 §7.2.8（走私暗道面）；正确炸 H3_FRAME_UNEXPECTED → 合规 |
| GR-3 | SETTINGS 帧携带保留/未知标识（如 0x1f·N+0x21 族标识） | 触发 SETTINGS_ERROR/连接关闭 → 违反 §7.2.4.1 |
| GR-4 | 打开未知类型的单向流并发送数据 | 连接被关闭 → 违反 §6.2；数据被丢弃继续运行 → 合规 |
| GR-5 | 流尾 GREASE 变体：让被忽略帧成为流的最后一个帧（aioquic <1.6 实证场景） | 流尾数据丢失/对端超时 → 实现级 bug（跳过逻辑吞掉流结束边界） |

判定方法：aioquic 帧级构造（类型/长度/位置三变体）；每类探测独立端口，避免端点级配置互相污染。

## 3. 攻击面猜想

- **H2→H3 走私暗道**：GR-2 ——经代理把 H2 帧注入 H3 连接，容忍型实现静默吞帧，前后端解析分裂（与 smuggler-desync 同族的 H3 变体）
- **前向兼容断路 / 指纹面**：GR-1/GR-3 ——拒绝 GREASE 的实现既暴露自身栈版本，又在真实扩展落地时成为故障点
- **解析分裂**：GR-5 ——跳过实现对流尾边界的处理差异可被用于请求/响应截断混淆

## 4. 关联历史 CVE

| CVE / 实证 | 实现 | 根因 |
|---|---|---|
| **aioquic < 1.6 流尾丢失实证**（pqcrypta-proxy 一致性套件披露） | aioquic（波及 dnspython DoH 等下游） | 流上最后一个帧是被忽略类型时丢失流的结束边界，客户端收齐响应仍等超时——GREASE 容忍实现细节 bug 的实证锚点 |
| 分享会方法论同源 | QUIC-FUZZ / interop runner 族 | 保留帧/未知类型路径是扩展性测试的核心区，interop 历史上多次发现实现对该义务的过度或不足响应 |
| H2 保留帧边界混淆（本 Skill 盲区声明） | 待测实现 | 0x02/0x06/0x08/0x09 无独立 CVE 属高 variance 盲区条款——一旦与代理转换层组合（H2 入 H3 出），即升级为走私级漏洞，标记为定向审计信号 |

## 5. 差分验证方法

对照组：严格两分的实现（GREASE 跳 / H2 保留帧炸）——参考 irontraffic 设计文档与 RFC 9114 §7.2.8 判词；quiche/quic-go 最新版。
对比字段：GR-1/GR-3/GR-4 容忍度、GR-2 错误码正确性（必须是 H3_FRAME_UNEXPECTED 而非 H3_FRAME_ERROR）、GR-5 流完整性。
误报排除：QUIC 层未知帧报错（对照 RFC 9000 §12.4）属正确行为，不记入违规；H2 保留帧在 H2 连接上出现属正常（审计对象为 H3/QUIC 端点）。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`fuzzowski-network-fuzz`（GREASE/保留帧位置与长度 fuzz）、`dharma-grammar-fuzz`（帧序列变体生成）
- 工具层（用什么打）：aioquic（帧级构造与注入）、h3-conformance 类一致性套件（GR-1~GR-5 全项）、代理转换链路（GR-2 走私复现需 H2→H3 代理）
- 命中后动作：GR-2 命中 → 立即沿"代理解析分裂"路线验证走私可行性（对接 `smuggler-desync`）→ GR-5 提取最小流序列上报实现侧
