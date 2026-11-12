---
name: hash-attack-techniques
description: "Hash attacks: length extension, MD5/SHA1 collisions, HMAC timing leaks, birthday attacks, hash proof-of-work for CTF/auth testing. Signals: hash attack, length extension, hash collision, HMAC timing, MD5 collision."
zh-signals: "哈希攻击:长度扩展、MD5/SHA1 碰撞、HMAC 时序泄露、生日攻击、哈希工作量证明(CTF/授权测试)。信号:哈希攻击,长度扩展,哈希碰撞,hmac时序,md5碰撞。"
when-to-use: >-
  Hash attack playbook. Use when exploiting length extension, MD5/SHA1
  collisions, HMAC timing leaks, birthday attacks, or hash-based proof
  of work in CTF and authorized testing scenarios.
---

# SKILL: Hash Attack Techniques — Expert Cryptanalysis Playbook

> **AI LOAD INSTRUCTION**: Expert hash attack techniques for CTF and security assessments. Covers length extension attacks, MD5/SHA1 collision generation, meet-in-the-middle hash attacks, HMAC timing side channels, birthday attacks, and proof-of-work solving. Base models often incorrectly apply length extension to HMAC or SHA-3, or fail to distinguish between identical-prefix and chosen-prefix collisions.

## 0. RELATED ROUTING

- [rsa-attack-techniques](../rsa-attack-techniques/SKILL.md) when hash weaknesses affect RSA signature schemes
- [symmetric-cipher-attacks](../symmetric-cipher-attacks/SKILL.md) when hash is used in key derivation
- [classical-cipher-analysis](../classical-cipher-analysis/SKILL.md) when analyzing hash-like constructions in classical ciphers

### Quick attack selection

| Scenario | Attack | Tool |
|---|---|---|
| `H(secret \|\| msg)` known, extend message | Length extension | HashPump, hash_extender |
| Need two files with same MD5 | Identical-prefix collision | fastcoll |
| Need specific MD5 prefix match | Chosen-prefix collision | hashclash |
| Byte-by-byte HMAC comparison | Timing attack | Custom script |
| Find any collision | Birthday attack | O(2^(n/2)) |
| Proof of work: find hash with leading zeros | Brute force | hashcat, Python |

---

## 1. LENGTH EXTENSION ATTACK

### 1.1 Vulnerable vs Non-Vulnerable

| Hash | Vulnerable | Why |
|---|---|---|
| MD5 | Yes | Merkle-Damgard construction |
| SHA-1 | Yes | Merkle-Damgard construction |
| SHA-256 | Yes | Merkle-Damgard construction |
| SHA-512 | Yes | Merkle-Damgard construction |
| SHA-3 / Keccak | No | Sponge construction |
| HMAC-* | No | Double hashing prevents extension |
| SHA-256 truncated | No (if truncated) | Missing internal state bits |
| BLAKE2 | No | Different construction |

### 1.2 Attack Mechanism

```
Given:   MAC = H(secret || original_message)
Known:   original_message, len(secret), MAC value
Compute: H(secret || original_message || padding || extension)
         WITHOUT knowing the secret!

How: The MAC value IS the internal hash state after processing
     (secret || original_message || padding).
     Initialize hash with this state, continue hashing extension.
```

### 1.3 Padding Calculation (MD5/SHA)

```python
def md5_padding(message_len_bytes):
    """Calculate MD5/SHA padding for given message length."""
    bit_len = message_len_bytes * 8

    # Pad with 0x80 + zeros until length ≡ 56 (mod 64)
    padding = b'\x80'
    padding += b'\x00' * ((55 - message_len_bytes) % 64)

    # Append original length as 64-bit little-endian (MD5)
    # or big-endian (SHA)
    padding += bit_len.to_bytes(8, 'little')  # MD5
    # padding += bit_len.to_bytes(8, 'big')    # SHA

    return padding
```

### 1.4 Tool Usage

```bash
# HashPump
hashpump -s "known_mac_hex" \
         -d "original_data" \
         -k 16 \            # secret length
         -a "extension_data"

# Output: new_mac, new_data (original + padding + extension)

# hash_extender
hash_extender --data "original" \
              --secret 16 \
              --append "extension" \
              --signature "known_mac_hex" \
              --format md5
```

### 1.5 Python Implementation

```python
import struct

def md5_extend(original_mac, original_data_len, secret_len, extension):
    """
    Perform MD5 length extension attack.
    original_mac: hex string of H(secret || original_data)
    """
    # Parse MAC into MD5 internal state (4 × 32-bit words, little-endian)
    h = struct.unpack('<4I', bytes.fromhex(original_mac))

    # Calculate total length after padding
    total_original = secret_len + original_data_len
    padding = md5_padding(total_original)
    forged_len = total_original + len(padding) + len(extension)

    # Continue MD5 from saved state with extension
    # (requires MD5 implementation that accepts initial state)
    from hashlib import md5
    # Most stdlib md5 doesn't expose state setting
    # Use: hlextend library or custom MD5

    import hlextend
    sha = hlextend.new('md5')
    new_hash = sha.extend(extension, original_data, secret_len,
                          original_mac)
    new_data = sha.payload  # includes original + padding + extension

    return new_hash, new_data
```

---

## 2. MD5 COLLISION ATTACKS

### 2.1 Identical-Prefix Collision (fastcoll)

Two messages with same prefix but different content, producing identical MD5.

```bash
# Generate collision pair
fastcoll -p prefix_file -o collision1.bin collision2.bin

# Result: MD5(collision1.bin) == MD5(collision2.bin)
# Files differ in exactly 128 bytes (two MD5 blocks)
```

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.
