---
name: ctf-reverse
description: "CTF reverse engineering. Triggers: IDA/Ghidra decompilation, PE/ELF analysis, algorithm reversing, dynamic debugging, unpacking, binary patching, and similar scenarios."
zh-signals: "CTF 逆向工程分析。信号:CTF,逆向,IDA,Ghidra,脱壳,动态调试"
when-to-use: "Use for CTF reverse challenges involving IDA or Ghidra decompilation, PE/ELF analysis, algorithm reversing, dynamic debugging, unpacking, or binary patching."
---

# ctf-reverse — CTF Reverse Engineering

## 1. Basic Toolchain

```bash
# File analysis
file challenge
strings challenge | grep -i flag
strings challenge | head -50

# Detect packer
rabin2 -I challenge        # rabin2 (r2)
upx -d challenge           # try to unpack a UPX packer
```

**Common tools**:
- **IDA Pro / IDA Free** — the most powerful decompiler
- **Ghidra** — NSA open-source reverse engineering tool, free
- **x64dbg / OllyDbg** — Windows dynamic debugging
- **gdb / pwndbg / gef** — Linux dynamic debugging
- **radare2 / cutter** — command-line reverse engineering framework

## 2. Analysis Workflow

```
1. file + strings for an initial assessment (language, architecture, packed or not)
2. Run the program and observe its behavior
3. Statically analyze the main logic in IDA/Ghidra
4. Use dynamic debugging to locate the key functions
5. Write a reversing script or patch the program directly
```

## 3. Common Algorithm Reversing

### Simple algorithms (arrays / loops)

```python
# Observe the for loop in IDA
# Locate the key array and the indices
data = [...]
for i in range(len(data)):
    data[i] = (data[i] ^ key[i % keylen]) - 0x20
print(''.join(chr(c) for c in data))
```

### Base64 variants

```python
import base64
custom_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
# Replace the letter order
import codecs
codecs.encode(b"data", "base64")
```

### Custom encryption

```python
def decrypt(data, key):
    out = []
    for i, c in enumerate(data):
        out.append((c ^ key[i % len(key)]) - 0x10)
    return bytes(out)
```

### TEA/XTEA/XXTEA

```python
# Find the signature: DELTA = 0x9E3779B9 (the TEA constant)
# A 32-round loop
```

## 4. Dynamic Debugging

### GDB / pwndbg

```bash
gdb ./challenge
# or pwndbg
pwndbg ./challenge

# Common commands
break main          # breakpoint
break *0x08048484  # address breakpoint
run                 # run
nexti / ni          # step over
stepi / si          # step into function
info registers      # view registers
x/20x 0x08048000   # memory view (hex)
x/s 0x08048000     # memory view (string)
continue / c        # continue execution
finish              # run until the function returns
```

### Dynamic Patching with Python Scripts

```python
from pwn import *

p = process('./challenge')
# or remote
# p = remote('host', port)

# Send input
p.sendline(b'A' * 100)

# Interactive debugging
p.interactive()
```

## 5. Unpacking

### UPX Unpacking

```bash
upx -d challenge -o challenge_unpacked
# If a custom packer is used, unpack it manually
```

### Manual Unpacking Workflow

```
1. Find the OEP (Original Entry Point)
   - Single-step in the debugger until you reach the real program entry
   - OEP signature: a jump to the OEP after a long run of pushad / pushfd

2. Dump memory
   - Break at the OEP
   - Dump all memory segments with a dumping tool

3. Fix the IAT (Import Address Table)
   - Rebuild the import table
```

## 6. Patching and Modification

```python
from pwn import *

elf = ELF('./challenge')
# Patch a function
elf.asm(elf.symbols['check'], 'ret')

# Patch a byte
elf.patch_byte(0x08048567, 0x90)  # NOP

elf.save()
```

## 7. Common Reversing Patterns

```
- String comparison → locate the key function → bypass it
- Maze problem → extract the map → find the path
- Virtual machine protection → analyze the opcodes → emulate execution
- Custom instruction set → reverse the bytecode
- Encryption algorithm → extract the key → decrypt
```

## 8. Solution Template

```python
data = [0x66, 0x6B, 0x63, 0x64, 0x7F, 0x6B]  # extracted data
key = [1, 2, 3]

result = []
for i in range(len(data)):
    result.append((data[i] ^ key[i % len(key)]) - 3)

print(''.join(chr(c) for c in result))
```
