---
name: symmetric-cipher-attacks
description: "对称密码攻击:CBC padding oracle、ECB 切块重排、比特翻转、流密钥重用、中间相遇。信号:对称密码,padding oracle,ecb,比特翻转,密钥重用。"
when-to-use: >-
  Symmetric cipher attack playbook. Use when exploiting block cipher mode
  weaknesses (CBC padding oracle, ECB cut-and-paste, bit flipping), stream
  cipher key reuse, or meet-in-the-middle attacks.
---

# SKILL: Symmetric Cipher Attacks — Expert Cryptanalysis Playbook

> **AI LOAD INSTRUCTION**: Expert techniques for attacking symmetric encryption in CTF and authorized testing. Covers CBC padding oracle, CBC bit flipping, ECB detection and exploitation, stream cipher key reuse, LFSR/LCG state recovery, RC4 biases, and meet-in-the-middle attacks. Base models often confuse ECB and CBC attack strategies or fail to set up byte-at-a-time ECB decryption correctly.

## 0. RELATED ROUTING

- [rsa-attack-techniques](../rsa-attack-techniques/SKILL.md) when symmetric key is protected by RSA
- [hash-attack-techniques](../hash-attack-techniques/SKILL.md) when HMAC or hash-based authentication is involved
- [lattice-crypto-attacks](../lattice-crypto-attacks/SKILL.md) for LCG/LFSR state recovery via lattice methods

### Advanced Reference

Also load BLOCK_CIPHER_ATTACKS.md when you need:
- Detailed attack scripts with full Python implementations
- Step-by-step byte-at-a-time ECB walkthrough
- PadBuster usage and custom padding oracle scripts
- LCG/LFSR recovery implementation

### Quick attack selection

| Observable Behavior | Likely Weakness | Attack |
|---|---|---|
| Same plaintext → same ciphertext (block-aligned) | ECB mode | Cut-and-paste / byte-at-a-time |
| Padding error distinguishable | CBC padding oracle | Decrypt without key |
| Can modify ciphertext, affects next block | CBC mode, no integrity check | Bit flipping |
| Key reused with XOR/stream cipher | Two-time pad | XOR ciphertexts together |
| Predictable PRNG output | LCG or LFSR | State recovery |
| Double encryption used | 2DES-like | Meet in the middle |

---

## 1. PADDING ORACLE ATTACK (CBC MODE)

### 1.1 Mechanism

CBC decryption: `P_i = D_K(C_i) ⊕ C_{i-1}`

If the server reveals whether padding is valid (PKCS#7), we can decrypt any block by manipulating the previous ciphertext block.

### 1.2 Attack Steps

```
Target: decrypt block C_i (with unknown plaintext P_i)

For byte position b = 15 down to 0 (last byte first):
  padding_value = 16 - b
  
  For guess = 0x00 to 0xFF:
    Construct modified C'_{i-1}:
      - Bytes 0..b-1: original C_{i-1} bytes
      - Byte b: guess
      - Bytes b+1..15: calculated to produce correct padding
    
    Send (C'_{i-1} || C_i) to oracle
    
    If oracle says "valid padding":
      intermediate_byte[b] = guess ⊕ padding_value
      plaintext_byte[b] = intermediate_byte[b] ⊕ original_C_{i-1}[b]
```

### 1.3 Python Implementation

```python
def padding_oracle_attack(ciphertext, block_size, oracle):
    """
    oracle(ct) returns True if padding is valid, False otherwise.
    ciphertext includes IV as first block.
    """
    blocks = [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]
    plaintext = b""

    for block_idx in range(1, len(blocks)):
        prev_block = bytearray(blocks[block_idx - 1])
        curr_block = blocks[block_idx]
        intermediate = [0] * block_size
        decrypted = [0] * block_size

        for byte_pos in range(block_size - 1, -1, -1):
            padding_val = block_size - byte_pos

            for guess in range(256):
                modified = bytearray(block_size)
                modified[byte_pos] = guess

                for j in range(byte_pos + 1, block_size):
                    modified[j] = intermediate[j] ^ padding_val

                test_ct = bytes(modified) + curr_block
                if oracle(test_ct):
                    if byte_pos == block_size - 1:
                        # Verify it's not a false positive (padding 0x02 0x02)
                        check = bytearray(modified)
                        check[byte_pos - 1] ^= 1
                        if not oracle(bytes(check) + curr_block):
                            continue

                    intermediate[byte_pos] = guess ^ padding_val
                    decrypted[byte_pos] = intermediate[byte_pos] ^ prev_block[byte_pos]
                    break

        plaintext += bytes(decrypted)

    return plaintext
```

### 1.4 Tools

```bash
# PadBuster
padbuster http://target/decrypt?ct= CIPHERTEXT_HEX 16 -encoding 0
padbuster http://target/decrypt?ct= CIPHERTEXT_HEX 16 -encoding 0 -plaintext "admin=true"
```

---

## 2. CBC BIT FLIPPING

### 2.1 Concept

Flipping bit at position j in C_{i-1} flips the same bit at position j in P_i (and corrupts all of P_{i-1}).

```
Original:  P_i[j] = D_K(C_i)[j] ⊕ C_{i-1}[j]
Modified:  P'_i[j] = D_K(C_i)[j] ⊕ C'_{i-1}[j]
                    = P_i[j] ⊕ (C_{i-1}[j] ⊕ C'_{i-1}[j])
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

> 📎 **参考文档说明**：本 skill 转自上游开源仓库，以下参考文档**未随本库分发**：`BLOCK_CIPHER_ATTACKS.md`。相关主题的要点已保留在本文对应描述中；如需展开内容，请按正文关键词在库内 grep 或自行检索。
