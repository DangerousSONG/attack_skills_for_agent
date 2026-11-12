---
name: cache-poisoning-smuggling
description: "Web cache poisoning and HTTP request smuggling. Use when the target uses a CDN/reverse proxy/cache layer (Cloudflare/Varnish/Nginx), or when front-end and back-end server behavior differs. Poison the cache or bypass security controls by manipulating cache keys or exploiting HTTP parsing differences. Advanced web attack techniques"
zh-signals: "利用缓存键之外的输入投毒 Web 缓存，或借助前后端 HTTP 解析差异实施请求走私。信号:缓存投毒,请求走私,CDN,反代,解析差异"
when-to-use: >-
  Use when a target sits behind a CDN, reverse proxy, or cache layer, or when front-end
  and back-end server behavior differs enough to allow cache poisoning or HTTP desync.
metadata:
  tags: "cache poisoning,request smuggling,http smuggling,cache-poisoning,request-smuggling,cdn,desync,cl-te,te-cl,hop-by-hop"
  category: "exploit"
---

# Web Cache Poisoning & HTTP Request Smuggling

Two related but distinct advanced web attack techniques, both of which exploit parsing differences in multi-tier web architectures.

---

## Part A: Web Cache Poisoning

Core idea: find an **HTTP header that influences the response content but is not included in the cache key** (unkeyed input), and inject malicious content into the cache.

### A.1 Identify Cache Behavior
```
# Send the same request twice and inspect the response headers
http_request url="http://target/page" headers={"X-Test":"1"}
```
Cache indicators:
- `X-Cache: HIT/MISS`
- `Age: 300` (cache age in seconds)
- `CF-Cache-Status: HIT` (Cloudflare)
- `Via: 1.1 varnish`

### A.2 Discover Unkeyed Input
Test HTTP headers one by one to see whether they influence the response without changing the cache key:

```
X-Forwarded-Host: evil.com     → does evil.com appear in the response?
X-Forwarded-Scheme: http       → forces an HTTP redirect?
X-Original-URL: /admin         → path override?
X-Rewrite-URL: /admin
X-Forwarded-For: 127.0.0.1    → bypasses IP restrictions?
```

### A.3 Poisoning
If `X-Forwarded-Host` influences the resource links in the response:
1. Send a request with the malicious header
2. The response gets cached (with the malicious content)
3. Later visitors requesting the same URL → they receive the poisoned cache

---

## Part B: HTTP Request Smuggling

Core idea: the front-end proxy and the back-end server disagree on how they parse **request boundaries**, so one HTTP request gets parsed as two.

### B.1 Identify the Smuggling Type

| Type | Front-end length source | Back-end length source |
|------|-------------|-------------|
| CL.TE | Content-Length | Transfer-Encoding |
| TE.CL | Transfer-Encoding | Content-Length |
| TE.TE | Transfer-Encoding | Transfer-Encoding (handling difference)|

### B.2 CL.TE Detection

The front-end uses Content-Length, the back-end uses Transfer-Encoding:
```
POST / HTTP/1.1
Host: target.com
Content-Length: 13
Transfer-Encoding: chunked

0

SMUGGLED
```
If the back-end processes `SMUGGLED` as the start of a new request → smuggling exists.

**Time-delay detection method** (more reliable): send an incomplete chunked body; if the front-end forwards it according to CL while the back-end waits for the remaining chunks → response timeout/time delay → CL.TE smuggling exists. The response difference (timeout vs. normal) is the key evidence.

### B.3 TE.CL Detection
```
POST / HTTP/1.1
Host: target.com
Content-Length: 3
Transfer-Encoding: chunked

8
SMUGGLED
0


```

### B.4 Exploiting the Smuggling

**Bypassing front-end security controls**:
Smuggle a request to `/admin` to bypass the front-end proxy's ACL.

**Stealing other users' requests**:
Smuggle an incomplete POST request so the back-end waits for more data → the next user's request gets appended → read its Cookie/Token.

**Cache poisoning**:
Smuggle a request to a different path so the cache stores the wrong response content.

## Notes
- HTTP smuggling requires precise control of raw HTTP bytes — send with curl `--data-binary`
- The blast radius of cache poisoning depends on the TTL and the key design
- TE.TE obfuscation bypasses: `Transfer-Encoding: xchunked`, `Transfer-Encoding\n: chunked` (newline/folding injection), multiple TE headers exploiting parsing differences
- After cache poisoning you can inject XSS and load malicious JS that affects all visitors

## Further Reading

- Advanced cache poisoning/smuggling techniques (Web Cache Deception/HTTP/2 Downgrade/h2c/Response Desync) → [references/cache-smuggling-techniques.md](references/cache-smuggling-techniques.md)
