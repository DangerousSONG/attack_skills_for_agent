---
name: rfc9114-pseudo-header-field-validation
description: 审计 HTTP/3 目标对畸形伪头/字段的处理是否严格按 RFC 9114 §4.1.2/§4.2/§4.3 判 malformed——宽容处理即存在解析分裂与 H3→H1 走私攻击面
rfc: RFC 9114 §4.1.2 / §4.2 / §4.3 / §10.3
license: Apache-2.0
---

# RFC 9114 伪头与字段校验严格性审计（malformed 判定完备性）

## 1. 约束条款（原文出处）

RFC 9114 §4.1.2，malformed 情形清单（非穷尽）：

> the presence of prohibited fields or pseudo-header fields / the absence of mandatory pseudo-header fields / invalid values for pseudo-header fields / pseudo-header fields after fields / an invalid sequence of HTTP messages / the inclusion of uppercase field names / the inclusion of invalid characters in field names or values

> 任何被检测到的 malformed 请求或响应 MUST be treated as a stream error of type H3_MESSAGE_ERROR。中介者 MUST NOT 转发。

§4.3：伪头字段必须出现在常规字段之前（否则 malformed）；请求伪头不得出现在响应中，反之；**伪头不得出现在 trailer 区块**；未定义/无效伪头必须判 malformed。

§4.2：字段名必须小写，含大写必须判 malformed；**HTTP/3 消息不得包含 connection-specific 字段**（如 Connection、Transfer-Encoding 语义），出现即 malformed。

§10.3：H3 的字段编码可表达 H1 语法无效的字段名；含无效字段名的消息必须判 malformed，因此中介者**无法**将其转换为 H1 消息——试图转换即引入解析歧义。

RFC 原文强调这些要求"deliberately strict because being permissive can expose implementations to these vulnerabilities"。

## 2. 违规判定条件

| 编号 | 探测 | 判定 |
|---|---|---|
| PH-1 | 缺 :method / :scheme / :path；或伪头置于常规字段之后 | 未以 H3_MESSAGE_ERROR 关闭流 → 违规 |
| PH-2 | 字段名含大写（如 `X-Custom: v` → `X-CuStOm`）、非法字符 | 同上 |
| PH-3 | 请求携带 connection-specific 字段（connection、keep-alive、TE 非 trailers、upgrade 等） | 同上 |
| PH-4 | trailer 区块中出现伪头字段 | 同上 |
| PH-5 | 经 H3 代理转换为 H1 后，H1 后端收到的请求是否"忠实"（大写被规范化了吗？非法字段被剥离了吗？） | 转换引入语义变化 → 解析分裂面 |
| PH-6 | 未知伪头（如 :foo） | 必须判 malformed |

判定方法：h3i 逐字段构造；对照 `RESET_STREAM` 错误码。

## 3. 攻击面猜想

每类宽容都是一个 H3 前端与 H1 后端之间的**解析分歧点**，组合起来即 H3→H1 请求走私/缓存投毒的原语库。PH-3（connection-specific 字段）在 H1 侧会激活 hop-by-hop 语义（如 TE: chunked），是转换型代理最危险的宽容面。NGINX 的公开未修复行为（见下）说明实现普遍不完整。

## 4. 关联历史 CVE / 公开案例

| 案例 | 实现 | 说明 |
|---|---|---|
| nginx/nginx#1043（issue，未修复） | NGINX | 违反 §4.1.2：畸形伪头请求未以 H3_MESSAGE_ERROR 关闭流——说明头部实现的 malformed 判定普遍不全 |
| CVE-2026-33555 的同类根因 | HAProxy | FIN 路径绕过 body 校验，属"malformed 判定覆盖不全"的变体（详见 rfc9114-content-length-data-mismatch） |
| 历史模式（H2 侧） | 多家 | RFC 7540 时代"伪头/字段校验不严格 → 走私"（如 CVE-2019-* 系列 H2 实现差异），H3 实现复刻了同样的错误 |

## 5. 差分验证方法

对照组：quic-go（malformed 判定完备）、h3i 自带的预期行为。
对比字段：PH-1~PH-6 逐项打勾矩阵；代理目标额外记录 H1 后端实际收到的字节级请求。
误报排除：服务端发送 HTTP 错误响应后再关流是 §4.1.2 允许的（MAY），不算违规。

## 6. 对接的攻击 Skill

- 方法论：技能层「请求走私 / HTTP Desync」+「Web 应用漏洞利用」大类（Router 映射 slug）
- 工具：h3i（逐字段构造主力）、aioquic
- 命中后动作：把每项违规标记为走私原语，组合 PH-x 分歧做端到端走私验证
