---
name: rfc9113-stream-state-machine
description: 审计 HTTP/2 流状态机对非法帧迁移的处置——half-closed(remote) 收 DATA 等违规帧必须回 STREAM_CLOSED，攻击者批量制造即 MadeYouReset 资源消耗（CVE-2025-5115 Jetty GHSA-mmxm-8w33-wc4h）；HEADERS+RST_STREAM 竞态双回调双清可致 double-free（Apache h2_mplx.c，2026 披露）；RST_STREAM 的 refused-stream 路径在作用域内强制写可致堆 UAF（CVE-2026-56848 Node.js，修复 commit ba6cb5c）；持续 RST 洪流致连接关闭内存泄漏（CVE-2023-45802 Apache）；RFC 9113 §5.1 状态迁移表是判定锚点，但"合法 RST 与竞态帧交错"的正确收敛全靠实现
rfc: RFC 9113 §5.1（流状态）/ §5.4（错误处理）/ §6.4（RST_STREAM）
license: Apache-2.0
---

# RFC 9113 §5.1 流状态机非法迁移审计

## 1. 约束条款（原文出处）

RFC 9113 §5.1（要点）：
> idle 流收到 HEADERS/PRIORITY 以外的帧 → 连接错误 PROTOCOL_ERROR；half-closed(remote) 流收到 WINDOW_UPDATE/PRIORITY/RST_STREAM 以外的帧 → **流错误 STREAM_CLOSED**；reserved 流收发越界帧 → 连接错误。

RFC 9113 §5.1.1（要点）：
> 流 ID 不得复用；closed 流窗口更新可忽略（容忍期），其余帧按 STREAM_CLOSED。

核心模式一句话：**H2 的流状态机是一张清晰的迁移表，但每个"必须回错误"的非法迁移都是服务端的一次资源支出——攻击者批量制造非法帧，让服务端替它跑错误处理路径（分配 RST、跑回调、走清理），就是 MadeYouReset。更危险的是合法帧竞态：HEADERS 紧跟 RST_STREAM，两个回调各自清理同一对象，状态机正确但生命周期管理 double-free。审计既查"非法帧处置合不合规"，也查"合规处置的代价是否被夹住"以及"竞态收敛是否有去重守卫"。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| SS-1 | half-closed(remote)/closed 流上批量发 DATA | 未按 STREAM_CLOSED 处置或处置成本随帧数线性无界 → CVE-2025-5115 同款（兼测是否计入并发上限豁免） |
| SS-2 | idle 流（未开流）发 DATA/SETTINGS 类流帧 | 未按 PROTOCOL_ERROR 连接错误断开 → §5.1 idle 处置缺失 |
| SS-3 | HEADERS + 同帧流立即 RST_STREAM（非零错误码）高速循环 | 竞态路径内存错误（double-free/UAF）或重复清理 → Apache 2026 / Node.js 同款 |
| SS-4 | 流 ID 回绕复用（超过 2^31 后复用旧 ID） | 实现未防复用 → §5.1.1 ID 唯一性失守（长连接攻击面） |
| SS-5 | reserved(local) 流收到 DATA（非法） | 未按连接错误处理 → 推送状态机越界 |
| SS-6 | trailers（END_STREAM HEADERS）后对该流再发帧 | 状态收敛错误 → 尾部帧序列缺陷（与 H3 侧 trailers skill 平行） |

判定方法：帧级脚本按状态矩阵遍历非法迁移；高速循环测资源斜率；堆检查器（ASan/jemalloc 采样）抓竞态内存错误。

## 3. 攻击面猜想

- **内存破坏**：SS-3 ——double-free/UAF 可升级为 RCE 前提（Apache h2_mplx 双清、Node.js 作用域内提交 RST 均为实证）
- **资源消耗 DoS**：SS-1 ——错误处理路径本身被武器化（MadeYouReset 家族，Jetty 全分支修复）
- **长连接状态污染**：SS-4/SS-6 ——流 ID 复用或尾部帧收敛错误导致跨请求状态串扰（向请求走私演进）

## 4. 关联历史 CVE

| CVE | 实现 | 根因 |
|---|---|---|
| **CVE-2025-5115** | Eclipse Jetty ≤9.4.57/≤10.0.25/≤11.0.25/≤12.0.21（GHSA-mmxm-8w33-wc4h，MadeYouReset） | 客户端发非法帧（0 增量 WINDOW_UPDATE、closed 流 DATA）→ 服务端合规回 RST_STREAM → 消耗不计并发上限 → 高速造流耗尽资源 |
| **CVE-2026-56848** | Node.js（修复 commit ba6cb5c "http2: defer rst stream while in scope"） | refused-stream 路径在 nghttp2 作用域内强制 SendPendingData → 堆 use-after-free；CVSS 7.5 |
| Apache double-free（2026 披露，h2_mplx.c） | Apache httpd mod_http2 | HEADERS+RST_STREAM 竞态：nghttp2 双回调各自调用 m_stream_cleanup，同一 h2_stream 指针两次入 purge 列表 → apr_pool 双释放 |
| **CVE-2023-45802** | Apache httpd | RST_STREAM 快速重置族：连接关闭路径内存泄漏，持续攻击累积耗尽 |

## 5. 差分验证方法

对照组：修复版 Jetty（GHSA-mmxm-8w33-wc4h 指定版本）；Node.js ≥ 含 ba6cb5c 版本。
对比字段：SS-1 错误处置码正确性与成本斜率、SS-3 竞态窗口（重复 1e5 次堆错误检出率）、SS-4 ID 复用防护。
误报排除：实现回 STREAM_CLOSED 但对该类帧有总量熔断（连接级）→ 判定通过；错误处置正确且成本与修复版持平 → 判定通过。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`fuzzowski-network-fuzz`（状态×帧类型矩阵 fuzz）、`slowhttptest-dos`（非法帧慢速流）
- 工具层（用什么打）：Python h2 帧级构造 + ASan/Valgrind 目标侧检测
- 命中后动作：SS-3 确认 → 立即转内存破坏利用评估（配合 C46 二进制利用类 skill）→ 最小触发序列归档；SS-1 确认 → 测"非法帧速率 × 资源消耗"致瘫参数
