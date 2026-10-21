---
name: ctf-crypto
description: Provides cryptography attack techniques for CTF challenges. Use when attacking encryption, hashing, signatures, ZKP, PRNG, or mathematical crypto problems involving RSA, AES, ECC, lattices, LWE, CVP, number theory, Coppersmith, Pollard, Wiener, padding oracle, GCM, key derivation, or stream/block cipher weaknesses.
when-to-use: Provides cryptography attack techniques for CTF challenges. Use when attacking encryption, hashing, signatures, ZKP, PRNG, or mathematical crypto problems involving RSA, AES, ECC, lattices, LWE, CVP, 
license: MIT
compatibility: Requires filesystem-based agent (Claude Code or similar) with bash, Python 3, and internet access for tool installation.
allowed-tools: Bash Read Write Edit Glob Grep Task WebFetch WebSearch
metadata:
  user-invocable: "false"
---

# CTF Cryptography

Quick reference for crypto CTF challenges. Each technique has a one-liner here; see supporting files for full details with code.

## Prerequisites

**Python packages (all platforms):**
```bash
pip install pycryptodome z3-solver sympy gmpy2 hashpumpy fpylll py_ecc
# Coppersmith (optional): pip install coppersmith
# Alternative Coppersmith lib: git clone https://github.com/jvdsn/crypto-attacks ~/.ctf-tools/crypto-attacks && pip install -r ~/.ctf-tools/crypto-attacks/requirements.txt
```

**Linux (apt):**
```bash
apt install hashcat
```

**macOS (Homebrew):**
```bash
brew install hashcat
```

**Manual install:**
- SageMath (optional — only for legacy Sage fallback snippets (collapsed sections)) — Linux: `apt install sagemath`, macOS: `brew install --cask sage`
- RsaCtfTool — `git clone https://github.com/RsaCtfTool/RsaCtfTool` (automated RSA attacks)
- crypto-attacks (Coppersmith) — `git clone https://github.com/jvdsn/crypto-attacks ~/.ctf-tools/crypto-attacks` + `pip install -r ~/.ctf-tools/crypto-attacks/requirements.txt` (alternative to `pip install coppersmith`)

> **Note:** `gmpy2` requires libgmp — Linux: `apt install libgmp-dev`, macOS: `brew install gmp`.

## Additional Resources

- [classic-ciphers.md](classic-ciphers.md) - Classic ciphers: Vigenere (+ Kasiski examination), Atbash, substitution wheels, XOR variants (+ multi-byte frequency analysis), deterministic OTP, cascade XOR, book cipher, OTP key reuse / many-time pad, variable-length homophonic substitution, grid permutation cipher keyspace reduction, image-based Caesar shift ciphers, XOR key recovery via file format headers
- [modern-ciphers.md](modern-ciphers.md) - Modern cipher attacks: AES (CFB-8, ECB leakage), CBC-MAC/OFB-MAC, padding oracle, S-box collisions, GF(2) elimination, LCG partial output recovery, affine cipher over composite modulus, AES-GCM with derived keys, AES-GCM nonce reuse (forbidden attack), Ascon-like reduced-round differential cryptanalysis, custom linear MAC forgery, CBC padding oracle (full block decryption), Bleichenbacher RSA PKCS#1 v1.5 padding oracle (ROBOT), birthday attack / meet-in-the-middle, CRC32 collision signature forgery, AES key recovery via byte-by-byte zeroing oracle, AES-CBC ciphertext forging via error-message decryption oracle
- [modern-ciphers-2.md](modern-ciphers-2.md) - Modern cipher attacks (Part 2): Blum-Goldwasser bit-extension oracle, hash length extension, compression oracle (CRIME-style), hash function time reversal via cycle detection, OFB mode invertible RNG backward decryption, weak key derivation via public key hash XOR, HMAC-CRC linearity attack, DES weak keys in OFB mode, SRP protocol bypass, modified AES S-Box brute-force, square attack on reduced-round AES, AES-ECB byte-at-a-time chosen plaintext, AES-ECB cut-and-paste block manipulation, AES-CBC IV bit-flip auth bypass, Rabin LSB parity oracle, PBKDF2 pre-hash bypass, MD5 multi-collision via fastcol
- [modern-ciphers-3.md](modern-ciphers-3.md) - Modern cipher attacks (Part 3): custom hash state reversal, CRC32 brute-force for small payloads, noisy RSA LSB oracle error correction, sponge hash MITM collision, CBC IV forgery + block truncation, padding oracle to CBC bitflip RCE, SPN S-box intersection attack, AES-CFB IV recovery from timestamp-seeded PRNG, three-round XOR protocol key cancellation, AES-CBC UnicodeDecodeError side-channel oracle, SHA-256 basis attack for XOR-aggregate hash bypass, custom MAC forgery via XOR block cancellation, HMAC key recovery via XOR+addition arithmetic
- [modern-ciphers-4.md](modern-ciphers-4.md) - Modern cipher attacks (Part 4): ChaCha20-Poly1305 nonce reuse forbidden attack over $2^{130}-5$ (RFC 8439, CTR $C_1\oplus C_2=P_1\oplus P_2$, Poly1305 $\sum c_i r^{n-i}$ via galois/sympy, 2-msg $ad=""$ vectors), partitioning-oracle / key-committing AEAD splitting lattice, sponge generality (SHA-3/Keccak $0x06$ vs $0x01$, Ascon/Gimli/Sparkle rate/capacity/rounds/pad table + endianness workflow), eSTREAM Trivium 1152-round warmup & cube attack outline (Grain)
- [stream-ciphers.md](stream-ciphers.md) - Stream cipher attacks: LFSR (Berlekamp-Massey, correlation attack, known-plaintext, Galois vs Fibonacci, Galois tap recovery via autocorrelation), RC4 second-byte bias, XOR consecutive byte correlation
- [rsa-attacks.md](rsa-attacks.md) - RSA attacks: small e (cube root), common modulus, Wiener's, Pollard's p-1, Hastad's broadcast, Hastad with linear padding (Coppersmith), Franklin-Reiter related message (e=3), Coppersmith linearly-related primes, Fermat/consecutive primes, multi-prime, restricted-digit, Coppersmith structured primes, Manger oracle, polynomial hash
- [rsa-attacks-2.md](rsa-attacks-2.md) - RSA attacks (specialized): RSA p=q validation bypass, cube root CRT gcd(e,phi)>1, factoring from phi(n) multiple, multiplicative homomorphism signature forgery, weak keygen via base representation, RSA with gcd(e,phi)>1 exponent reduction, batch GCD shared prime factoring, partial key recovery from dp/dq/qinv, RSA-CRT fault attack, homomorphic decryption oracle bypass, small prime CRT decomposition, Montgomery reduction timing attack, Bleichenbacher low-exponent signature forgery, RSA signature bypass with e=1 and crafted modulus
- [ecc-attacks.md](ecc-attacks.md) - ECC attacks: small subgroup, invalid curve, Smart's attack (anomalous, with Sage code), fault injection, clock group DLP, Pohlig-Hellman, ECDSA nonce reuse, Ed25519 torsion side channel, DSA nonce reuse, DSA key recovery via MD5 collision on k-generation, X25519 low-order points + all-zero check
- [dh-attacks.md](dh-attacks.md) - Classic finite-field DH: trivial g (0/1/p-1), Pohlig-Hellman when p-1 smooth, small-subgroup confinement / Lim-Lee static key recovery via CRT, static vs ephemeral + Logjam downgrade triage
- [zkp-and-advanced.md](zkp-and-advanced.md) - ZKP/graph 3-coloring, Z3 solver guide, garbled circuits, Shamir SSS, bigram constraint solving, race conditions, Groth16 broken setup, DV-SNARG forgery, KZG pairing oracle for permutation recovery, Shamir SSS reused polynomial coefficients
- [prng.md](prng.md) - PRNG attacks (foundational): MT19937, MT float recovery via GF(2) magic matrix for token prediction, LCG, GF(2) matrix PRNG, V8 XorShift128+ Math.random state recovery via Z3, middle-square, deterministic RNG hill climbing, random-mode oracle, time-based seeds, C srand/rand synchronization via ctypes, password cracking, logistic map chaotic PRNG
- [prng-attacks.md](prng-attacks.md) - PRNG attacks (CTF-era, 2017+): MT subset-sum seed recovery, MT19937 constraint propagation, Rule 86 cellular automaton reversal via Z3, Java LCG meet-in-the-middle partial modulo, LCG backward stepping via modular inverse, LFSR bit-fold ASCII parity, Z3 solve-time timing oracle, randcrack DSA k prediction, format-string PRNG seed offset, NTP-poisoned PRNG UUID XOR
- [historical.md](historical.md) - Historical ciphers (Lorenz SZ40/42, book cipher implementation)
- [advanced-math.md](advanced-math.md) - Advanced mathematical attacks (isogenies, Pohlig-Hellman, baby-step giant-step (BSGS) for general DLP, LLL, Merkle-Hellman knapsack via LLL, Coppersmith via Howgrave-Graham hg_matrix -> IntegerMatrix -> LLL -> sympy Poly (beta=0.5, monic check, flatter optional dim>100), quaternion RSA, GF(2)[x] CRT, S-box collision code, LWE lattice CVP attack, affine cipher over non-prime modulus, introspective CRC via GF(2) linear algebra)
- [lattice-and-lwe.md](lattice-and-lwe.md) - Lattice attack triage and workflow: LLL/BKZ/Babai, HNP from partial or biased nonces, truncated LCG state recovery, LWE embedding and CVP, Ring-LWE / Module-LWE recognition, NTRU lattice B=[[qI 0],[H I]] (negacyclic, BKZ, centered g), GGH embedding [[B 0],[c lambda]] sweep lambda, Mersenne AJPS p=2^n-1 n=11213 w=10 6x6 s=5, BDD predicate/LadderLeak >100 sigs 1-4 bits, orthogonal lattices, subset sum / knapsack, and common failure modes
- [post-quantum.md](post-quantum.md) - Post-quantum recognition: ML-KEM (Kyber) k=2/3/4 q=3329 etau dv, ML-DSA, Falcon, Module-LWE flattening, FO failure oracle, NTT, Kannan/Bai-Galbraith/Arora-Ge/estimator decision tree, Mersenne AJPS details
- [exotic-crypto.md](exotic-crypto.md) - Exotic algebraic structures (braid group DH / Alexander polynomial, monotone function inversion, tropical semiring residuation, Paillier cryptosystem, Hamming code helical interleaving, ElGamal universal re-encryption, FPE Feistel brute-force, icosahedral symmetry group cipher, Goldwasser-Micali replication oracle)
- [exotic-crypto-2.md](exotic-crypto-2.md) - Exotic algebraic structures (Part 2, 2017+): BB-84 QKD MITM, ElGamal trivial DLP (B=p-1), Paillier LSB oracle via homomorphic doubling, differential privacy noise cancellation, homomorphic encryption bit-extraction, ElGamal over matrices via Jordan normal form, OSS signature forgery via Pollard, Cayley-Purser decryption without private key, BIP39 partial mnemonic checksum brute force, Asmuth-Bloom CRT threshold recovery, Rabin with polynomial primes, LCG period detection, Vandermonde polynomial coefficient recovery

---

## When to Pivot

- If the real blocker is understanding a binary, obfuscated client, or weird VM, switch to `/ctf-reverse`.
- If the challenge is mostly packet carving, disk recovery, or stego extraction before any decryption starts, switch to `/ctf-forensics`.
- If the task is just implementing an exploit against a vulnerable network service after the crypto part is solved, switch to `/ctf-pwn` or `/ctf-web`.
- If the crypto challenge involves adversarial ML, model extraction, or neural-network-based ciphers, switch to `/ctf-ai-ml`.
- If the challenge is really an encoding puzzle, esoteric cipher, or polyglot trick rather than true cryptanalysis, switch to `/ctf-misc`.

## Quick Start Commands

```bash
# Identify cipher type
python3 -c "from Crypto.Util.number import *; n=<N>; print(f'bits={n.bit_length()}')"

# RSA quick check
python3 -c "from sympy import factorint; print(factorint(<n>))"  # Small factors?
openssl rsa -pubin -in key.pub -text -noout  # Extract n, e from PEM

# Quick factorization tools
python3 RsaCtfTool.py -n <n> -e <e> --uncipher <c>

# XOR analysis
python3 -c "from pwn import xor; print(xor(bytes.fromhex('<hex>'), b'flag{'))"

# Hash identification
hashid '<hash>'
hashcat --identify '<hash>'

# Quick factorization (sympy, primary)
python3 -c "from sympy import factorint; print(factorint(<n>))"
# Sage alternative: sage -c "print(factor(<n>))"
```

## Classic Ciphers

- **Caesar:** Frequency analysis or brute force 26 keys
- **Vigenere:** Known plaintext attack with flag format prefix; derive key from `(ct - pt) mod 26`. Kasiski examination for unknown key length (GCD of repeated sequence distances)
- **Atbash:** A<->Z substitution; look for "Abashed" hints in challenge name
- **Substitution wheel:** Brute force all rotations of inner/outer alphabet mapping
- **Multi-byte XOR:** Split ciphertext by key position, frequency-analyze each column independently; score by English letter frequency (space = 0x20)
- **Cascade XOR:** Brute force first byte (256 attempts), rest follows deterministically
- **XOR rotation (power-of-2):** Even/odd bits never mix; only 4 candidate states
- **Weak XOR verification:** Single-byte XOR check has 1/256 pass rate; brute force with enough budget
- **Deterministic OTP:** Known-plaintext XOR to recover keystream; match load-balanced backends
- **OTP key reuse (many-time pad):** `C1 XOR C2 XOR known_P = unknown_P`; crib dragging when no plaintext known
- **Homophonic (variable-length):** Multi-character ciphertext groups map to single plaintext chars. Find n-grams with identical sub-n-gram frequencies, replace with symbols, solve as monoalphabetic. See [classic-ciphers.md](classic-ciphers.md#variable-length-homophonic-substitution-asis-ctf-finals-2013).
- **Grid permutation cipher:** 5x5 grid with independent row/column permutations collapses keyspace to 5! x 5! = 14,400; brute-force in milliseconds. See [classic-ciphers.md](classic-ciphers.md#grid-permutation-cipher-keyspace-reduction-bsidessf-2026).
- **Image-based Caesar shift:** Pixel rows/columns shifted by per-strip offsets; compare original vs shifted image to extract ASCII-encoded flag from shift amounts. See [classic-ciphers.md](classic-ciphers.md#image-based-caesar-shift-ciphers-bsidessf-2026).
- **Polybius square cipher:** 5x5 grid maps letter pairs to plaintext; digits/coordinates encode positions. See [classic-ciphers.md](classic-ciphers.md#polybius-square-cipher-qiwi-infosec-2016).
- **XOR key recovery via file format headers:** File claims to be PDF/PNG/ZIP but `file` reports "data". XOR first bytes against expected magic bytes to derive repeating key; extend using trailer structures (`%%EOF`, IEND marker). See [classic-ciphers.md](classic-ciphers.md#xor-key-recovery-via-file-format-headers-metactf-flash-2026).

See [classic-ciphers.md](classic-ciphers.md) for full code examples.

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
