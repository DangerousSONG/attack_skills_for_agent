---
name: rfc7541-hpack-table-capacity
description: 审计 HPACK 动态表容量协商与尺寸更新时序是否按 RFC 7541 §4.2/§6.3——编码器选择值超 SETTINGS 上限必须判解码错误、尺寸更新必须出现在变更后第一个头块开头、多次变更必须信号化最小值（至多两次更新）；解释分歧即 COMPRESSION_ERROR 互操作炸弹与表驱逐漏洞（关联 nghttp2/nghttp2#1660 解释分歧实证；Google Cloud ALB 临时降级动态表缓解客户端 bug；apache.hc.core5 5.3.1 修复）
rfc: RFC 7541 §4.2（Maximum Table Size）/ §4.3 / §6.3（Dynamic Table Size Update）/ §7.3（内存消耗）+ RFC 9113 §6.5.2（SETTINGS_HEADER_TABLE_SIZE）
license: Apache-2.0
---

# RFC 7541 §4.2/§6.3 HPACK 动态表容量与尺寸更新时序审计

## 1. 约束条款（原文出处）

RFC 7541 §4.2（原文）：
> An encoder can choose to use less capacity than this maximum size (see Section 6.3), but the chosen size MUST stay lower than or equal to the maximum set by the protocol.

> This dynamic table size update MUST occur at the beginning of the first header block following the change to the dynamic table size. In HTTP/2, this follows a settings acknowledgment.

> In the case that this size is changed more than once in that interval, the smallest maximum table size that occurs in that interval MUST be signaled in a dynamic table size update. The final maximum size is always signaled, resulting in at most two dynamic table size updates.

RFC 7541 §6.3（原文）：
> The new maximum size MUST be lower than or equal to the limit determined by the protocol using HPACK. A value that exceeds this limit MUST be treated as a decoding error.

核心模式一句话：**动态表是编码器与解码器共享的一块有状态的内存——尺寸协商的任何解释分歧都会炸出 COMPRESSION_ERROR；而"更新必须出现在头块开头"这条时序约束是防止解码器用旧表解码新表内容的唯一闸门。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| HP-1 | 发送动态表尺寸更新 > 对端 SETTINGS_HEADER_TABLE_SIZE 的值 | 未按解码错误断开 → §6.3 违规（表上限被击穿，内存面失控） |
| HP-2 | SETTINGS 把表大小从 4096 改为 0 后，第一个头块**开头**未发尺寸更新（或更新出现在头块中间） | 未判 COMPRESSION_ERROR → §4.2 时序违规（nghttp2#1660 解释分歧核心场景） |
| HP-3 | 间隔内多次变更表大小（4096→0→4096），检查是否信号化最小值（0）且至多两次更新 | 直接信号化最终值导致解码器驱逐时机错误 → §4.2 违规（驱逐不同步 = 幽灵条目/引用失效） |
| HP-4 | 尺寸更新后引用被驱逐槽位的索引 | 解码器崩溃/错误条目 → 驱逐一致性缺陷（§4.3/§4.4 实现警告区） |
| HP-5 | 频繁 0↔4096 振荡更新（每头块一次） | 服务端 CPU 显著升高且驱逐表被清空 → 资源消耗面（RFC 7541 §7.3 明示攻击路径） |

判定方法：nghttp -v --header-table-size=0 复现 #1660；双实现对照解码同一字节流比对结果。

## 3. 攻击面猜想

- **互操作炸弹**：HP-2/HP-3 ——对严格实现发宽松字节流（或反向），以 COMPRESSION_ERROR 打挂连接；LB/代理场景下可定向熔断特定后端
- **内存面失控**：HP-1 ——表上限被击穿直接违反对解码器内存的承诺
- **CPU/驱逐振荡**：HP-5 ——RFC 7541 §7.3 明示的内存消耗攻击路径的变体

## 4. 关联历史 CVE

| CVE / 实证 | 实现 | 根因 |
|---|---|---|
| **nghttp2/nghttp2#1660**（2021-12，HAProxy 复现） | nghttp2 ↔ HAProxy 互操作 | SETTINGS_HEADER_TABLE_SIZE=0 时是否需要初始尺寸更新解释分歧 → COMPRESSION_ERROR 断连；RFC 文本与实现行为的多解性实证 |
| **Google Cloud ALB 缓解事件**（2024-10 前后披露） | Google 前端 + apache.hc.core5.http2 <5.3.1 | 客户端动态表 bug 迫使 Google 对全部经典/全球外部 ALB 临时降低动态表大小——一个 HPACK 尺寸协商 bug 的杀伤半径实证 |
| **apache.hc.core5 5.3.1 修复**（2024-10-12 合入） | Apache HttpComponents Core | 动态表尺寸变更信号化时序修复，与 #1660 同族 |

## 5. 差分验证方法

对照组：nghttp2 最新版、严格实现（按 RFC 7541 字面要求初始更新）。
对比字段：HP-1 错误判定、HP-2 零表场景行为、HP-3 三次变更序列处理、HP-5 振荡成本曲线。
误报排除：两端均宽松实现时互操作"成功"不构成合规证据——必须以 RFC 条文逐条判定；SETTINGS_HEADER_TABLE_SIZE=0 场景的争议性已标注（#1660 未定谳），该探测标记为"解释分歧信号"而非硬违规。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`fuzzowski-network-fuzz`（HPACK 指令序列 fuzz）、`dharma-grammar-fuzz`（尺寸更新/头块组合语法生成）
- 工具层（用什么打）：nghttp（--header-table-size 变体）、Python h2/hpack 库（字节级 HPACK 构造）
- 命中后动作：HP-2/HP-3 命中 → 定向互操作炸弹验证（严格对端 + 宽松本端组合）→ HP-5 测量驱逐振荡 CPU 成本 → 证据并入压缩层弱点族
