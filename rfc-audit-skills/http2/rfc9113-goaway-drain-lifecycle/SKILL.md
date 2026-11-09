---
name: rfc9113-goaway-drain-lifecycle
description: 审计 HTTP/2 连接终止生命周期（GOAWAY draining 与 RST_STREAM 竞态）——RST_STREAM 与 GOAWAY 并发触发写管线竞态可致工作线程永久阻塞直至线程池耗尽（CVE-2026-12611 Jetty GHSA-gpg9-4257-cfm3：HTTP2Flusher.terminated 被竞态重置为 null，入队项永不处理）；nginx 优雅关闭时 H2 连接漏发 GOAWAY 致 worker 卡死（2024-05 kaseiwang 补丁 + http2-grace-shutdown-test PoC）；RFC 9113 §6.8 规定双 GOAWAY 优雅关闭序列但竞态窗口与终止单向性是实现义务
rfc: RFC 9113 §6.8（GOAWAY）/ §6.4（RST_STREAM）/ §5.1（流状态机）
license: Apache-2.0
---

# RFC 9113 §6.8 GOAWAY draining 与终止竞态审计

## 1. 约束条款（原文出处）

RFC 9113 §6.8（要点）：
> GOAWAY 携带 last-stream-ID，ID 更大的在途流**可被**发送方重试；端点**应当**先发送 last-stream-ID 为最大值的 GOAWAY、等待至少 1 RTT 后再发送携带真实 last-stream-ID 的第二个 GOAWAY（优雅关闭序列）。

核心模式一句话：**连接终止是 H2 状态机里最容易写出竞态的路径——GOAWAY 说"不再接受新流"、draining 期间旧流还在跑、RST_STREAM 随时插进来砍掉一半状态。RFC 给了双 GOAWAY 序列，但"终止是单向转移"这个不变量全靠实现自己守护，一旦某个并发路径能把终止标志重置回去，写管线就永久卡死。**

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| GD-1 | 并发混合发送 RST_STREAM 与 GOAWAY（多流交错、多连接放大） | 工作线程随重复次数单调增长且不复原 → CVE-2026-12611 同款（线程 dump 见 flusher 阻塞栈） |
| GD-2 | GOAWAY 后继续在 last-stream-ID 以上开新流 | 服务端未忽略/未按序处置 → §6.8 last-stream-ID 语义缺失 |
| GD-3 | 服务端优雅关闭（reload/重启信号）瞬间新建慢速连接 | 连接漏发 GOAWAY 或永不进入关闭 → nginx 2024 同款，worker 卡在 shutting down |
| GD-4 | 收到 GOAWAY 后发送第二个 last-stream-ID 不同的 GOAWAY（双 GOAWAY 序列） | 实现不支持双 GOAWAY 或第二个被当作错误 → 优雅关闭序列不兼容（互操作缺陷） |
| GD-5 | draining 期间对 half-closed 流发 RST_STREAM | 流状态机未正确收敛 → §5.1 状态迁移缺陷（卡流占资源） |

判定方法：h2 客户端并发发帧脚本 + `nginx -s reload` 类信号注入；观测线程数/连接关闭时间；线程 dump 定位阻塞栈。

## 3. 攻击面猜想

- **线程池耗尽 DoS**：GD-1 ——无需高带宽，精确时序交错 RST/GOAWAY 即可让 Jetty 类线程池模型全灭
- **优雅关闭劫持**：GD-3 ——发布/重启窗口被慢速连接钉死，运维层面 DoS（滚动发布场景放大）
- **draining 资源驻留**：GD-2/GD-5 ——GOAWAY 后新流被忽略但连接保持，连接表/流表被 draining 连接长期占用

## 4. 关联历史 CVE

| CVE / 实证 | 实现 | 根因 |
|---|---|---|
| **CVE-2026-12611**（GHSA-gpg9-4257-cfm3） | Eclipse Jetty jetty-http2-server | RST_STREAM 与 GOAWAY 竞态把 HTTP2Flusher.terminated 重置回 null → 入队项永不处理，阻塞写累积至线程池耗尽、服务全停；CWE-400，全版本分支（9.x/10.x/11.x/12.x）修复 |
| nginx graceful shutdown 缺陷（2024-05，kaseiwang） | nginx（freenginx 补丁讨论，commit 7f18358cc） | `ngx_close_idle_connections` 与 `ngx_http_v2_init` 时间竞态 → 部分 H2 连接 c->idle 置位晚于关闭扫描，漏发 GOAWAY，worker 卡 shutting down；PoC 仓库 http2-grace-shutdown-test（15 秒慢连接 + reload 复现） |
| SwiftNIO 设计讨论（2024-02） | SwiftNIO | GOAWAY 与客户端开新流天然竞态 → 社区采用"GOAWAY(max) + PING + 1RTT + GOAWAY(真实)"双 GOAWAY 方案（RFC 推荐序列的实现参照） |

## 5. 差分验证方法

对照组：修复版 Jetty（GHSA-gpg9-4257-cfm3 指定版本）；nginx 应用 7f18358cc 补丁版。
对比字段：GD-1 线程数可复原件数、GD-3 关闭完成时间、GD-4 双 GOAWAY 兼容性。
误报排除：实现收到 GOAWAY 立即粗暴断连（无双 GOAWAY）→ 不优雅但不违规，记互操作缺陷不记安全违规；GD-1 重复 1000 次无线程增长 → 判定通过。

## 6. 对接的攻击 Skill

- 技能层（怎么打）：`slowhttptest-dos`（慢速连接 + 信号窗口叠加）、`fuzzowski-network-fuzz`（RST/GOAWAY 交错时序变异）
- 工具层（用什么打）：Python h2 并发帧构造、JVM 线程 dump / nginx worker 状态观测
- 命中后动作：GD-1 确认 → 测线程消耗速率与触发窗口概率 → 输出"连接数 × 重复次数"最小致瘫参数；GD-3 确认 → 关联发布流程做攻击窗口评估
