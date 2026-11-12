---
name: rsa-attack-techniques
description: "RSA attack playbook for CTF and real-world cryptanalysis. Signals: cryptographic attack, encryption cracking, weak randomness."
zh-signals: "RSA attack playbook for CTF and real-world cryptanalysis 信号:密码学攻击,加密破解,弱随机数。"
when-to-use: >-
  RSA attack playbook for CTF and real-world cryptanalysis. Use when given
  RSA parameters (n, e, c) and need to recover plaintext by exploiting
  weak keys, small exponents, shared factors, or padding oracles.
---

# SKILL: RSA Attack Techniques — Expert Cryptanalysis Playbook

> **AI LOAD INSTRUCTION**: Expert RSA attack techniques for CTF and authorized security assessments. Covers factorization attacks, small exponent exploits, lattice-based approaches (Wiener/Boneh-Durfee/Coppersmith), broadcast attacks, common modulus, padding oracles, and fault attacks. Base models often suggest attacks that don't match the given parameters or miss the correct attack selection based on what's known.

## 0. RELATED ROUTING

- [lattice-crypto-attacks](../lattice-crypto-attacks/SKILL.md) for deep lattice theory behind Coppersmith/Boneh-Durfee
- [hash-attack-techniques](../hash-attack-techniques/SKILL.md) when RSA signature forgery involves hash weaknesses
- [symmetric-cipher-attacks](../symmetric-cipher-attacks/SKILL.md) when RSA protects a symmetric key (hybrid encryption)

### Advanced Reference

Also load RSA_ATTACK_CATALOG.md when you need:
- Detailed SageMath/Python implementation for each attack
- Step-by-step mathematical derivation
- Edge cases and failure conditions per attack

### Quick attack selection

| Given / Observable | Attack | Tool |
|---|---|---|
| Small n (< 512 bits) | Direct factorization | factordb, yafu, msieve |
| e = 3, small message | Cube root | gmpy2.iroot |
| Multiple (n, c) same small e | Hastad broadcast | CRT + iroot |
| Very large e or very small d | Wiener / Boneh-Durfee | SageMath, RsaCtfTool |
| Partial p knowledge | Coppersmith small roots | SageMath |
| Same n, different e | Common modulus | Extended GCD |
| Multiple n values | Batch GCD (shared factor) | Python/SageMath |
| Padding error oracle | Bleichenbacher | Custom script |
| LSB parity oracle | LSB oracle attack | Custom script |
| Fault in CRT computation | RSA-CRT fault | Single faulty signature |

---

## 1. FACTORIZATION ATTACKS

### 1.1 Direct Factorization (Small n)

```python
from sympy import factorint

n = 0x...  # small modulus
factors = factorint(n)
p, q = list(factors.keys())
```

**When**: n < ~512 bits, or known to be in factordb.

### 1.2 Fermat's Factorization

Works when p and q are close together: |p - q| is small.

```python
from gmpy2 import isqrt, is_square

def fermat_factor(n):
    a = isqrt(n) + 1
    while True:
        b2 = a * a - n
        if is_square(b2):
            b = isqrt(b2)
            return (a + b, a - b)
        a += 1
```

### 1.3 Pollard's p-1

Works when p-1 has only small prime factors (B-smooth).

```python
from gmpy2 import gcd

def pollard_p1(n, B=2**20):
    a = 2
    for j in range(2, B):
        a = pow(a, j, n)
    d = gcd(a - 1, n)
    if 1 < d < n:
        return d
    return None
```

### 1.4 Batch GCD (Multiple n share a factor)

```python
from math import gcd
from functools import reduce

def batch_gcd(moduli):
    """Find shared factors among multiple RSA moduli."""
    product = reduce(lambda a, b: a * b, moduli)
    results = {}
    for i, n in enumerate(moduli):
        remainder = product // n
        g = gcd(n, remainder)
        if g != 1 and g != n:
            results[i] = (g, n // g)
    return results
```

---

## 2. SMALL EXPONENT ATTACKS

### 2.1 Cube Root Attack (e = 3, small m)

If m^e < n (no modular reduction occurred), simply take the e-th root.

```python
from gmpy2 import iroot

c = 0x...  # ciphertext
e = 3
m, exact = iroot(c, e)
if exact:
    print(f"Plaintext: {bytes.fromhex(hex(m)[2:])}")
```

### 2.2 Hastad Broadcast Attack

Same message encrypted with same small e under different moduli (n₁, n₂, ..., nₑ).

```python
from sympy.ntheory.modular import crt
from gmpy2 import iroot

# e = 3, three ciphertexts under three different n
n_list = [n1, n2, n3]
c_list = [c1, c2, c3]

# CRT: find x such that x ≡ ci (mod ni) for all i
r, M = crt(n_list, c_list)
m, exact = iroot(r, 3)
assert exact
```

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.

> 📎 **Reference Document Notice**: this skill is adapted from an upstream open-source repository; the following reference document is **not distributed with this library**: `RSA_ATTACK_CATALOG.md`. The key points of the related topics are retained in the corresponding descriptions in this document; if you need the expanded content, grep the library using keywords from the body text or search on your own.
