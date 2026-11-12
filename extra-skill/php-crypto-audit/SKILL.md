---
name: php-crypto-audit
description: "PHP web source code cryptographic and key security audit tool. Identifies weak hashing / weak encryption / hardcoded keys / signature verification flaws, and outputs severity ratings, PoC and remediation recommendations (must not be omitted)."
zh-signals: "审计 PHP 源码中的弱哈希、弱加密、硬编码密钥与签名校验缺陷。信号:PHP加密审计,弱哈希,硬编码密钥,JWT校验,签名缺陷。"
when-to-use: >-
  Use when reviewing a PHP codebase for cryptographic weaknesses such as MD5/SHA1 password hashing, insecure cipher modes, fixed IVs, hardcoded keys, or flawed JWT/HMAC signature verification.
---

# PHP Cryptography and Key Security Audit (php-crypto-audit)

Analyze the cryptographic and hashing implementations for passwords / tokens / sensitive data in PHP project source code, and detect:
- Weak hashing (MD5/SHA1/no salt)
- Insecure symmetric/asymmetric encryption usage (ECB, fixed IV, wrong mode)
- Signature verification flaws (JWT not verified, wrong HMAC usage, attacker-controllable algorithm selection)
- Hardcoded keys / plaintext key exposure

## Severity Rating and Numbering
- See `shared/SEVERITY_RATING.md` for details
- Vulnerability ID: `{C/H/M/L}-CRYPTO-{seq}`

## Mandatory Sinks to Check (Required)
You must search for and analyze the following implementation points (replace them with the project's actual equivalents):
- Password hashing: `md5/sha1/hash` (not `password_hash`), misuse of `crypt` parameters
- Secure hashing: `password_hash` / `password_verify` (check whether the parameters are correct)
- Symmetric encryption: `openssl_encrypt/decrypt` (check mode/iv)
- Signature: `hash_hmac`, `openssl_sign`, JWT verify / signature comparison implementations

## Mandatory Checks (Required)
- You must locate the "key source": hardcoded / environment variable / config file / request parameter
- You must judge "whether verification is reliable": whether the algorithm is attacker-controllable or the comparison leaks timing
- You must output remediation recommendations and a migration plan (e.g. upgrade the hashing algorithm, enforce parameterized modes)

## PoC (Required Framework)
Because cryptographic vulnerabilities may depend on the environment, the PoC must at minimum provide:
- An executable "verification framework" (e.g. construct a JWT payload and explain which verification failure / bypass should occur)
- Or observable evidence (e.g. log leakage, error patterns producing reversible results)

## Report Output
```
{output_path}/vuln_audit/crypto_{timestamp}.md
```
