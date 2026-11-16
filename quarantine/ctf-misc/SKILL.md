---
name: ctf-misc
description: "CTF Misc general. Triggered for scenarios involving steganography (LSB/Zsteg), traffic analysis (pcap/strings), memory forensics (volatility), archive attacks, log analysis, and similar."
zh-signals: "CTF Misc 综合技能，涵盖隐写术、流量分析、内存取证、压缩包攻击与日志分析。信号:CTF Misc,隐写术,流量分析,内存取证,压缩包"
when-to-use: "Use when solving CTF miscellaneous challenges involving steganography, pcap traffic analysis, memory forensics, archive attacks, or log analysis."
---

# ctf-misc — CTF Misc General Direction

## 1. Image Steganography

### Basic tools

```bash
file image.jpg
binwalk image.jpg          # Separate embedded files
binwalk -e image.jpg       # Automatic extraction
exiftool image.jpg         # Metadata
strings image.jpg | grep -i flag

# Image viewing
identify image.jpg
display image.jpg
```

### LSB steganography (least significant bit)

**zsteg (PNG/BMP)**
```bash
zsteg image.png            # Detect LSB
zsteg image.png -b 1       # Bit plane 1
zsteg image.png --lsb      # All layers
zsteg image.png --all      # Try everything
```

**Steghide**
```bash
steghide extract -sf image.jpg -p ""   # No password
steghide extract -sf image.jpg -p password
steghide info image.jpg
```

**StegSolve (Java GUI)**
```bash
java -jar StegSolve.jar
```

### PNG specifics

```bash
# CRC error repair (the CRC is broken after modifying width/height)
pngcheck -v image.png
python3 fixpng.py image.png   # Repair the CRC

# Modify the width/height in the IHDR chunk (hex editor)
```

## 2. Audio Steganography

```bash
# Spectrum analysis
audacity audio.wav
ffmpeg -i audio.mp3 -show_freqs audio.png

# Convert the spectrogram to an image
sox audio.wav -n spectrogram -o spectrogram.png

# Extract data
strings audio.mp3 | grep -i flag
```

**Morse code**: look for dots and dashes in the waveform, or use the `morse2ascii` tool

## 3. Traffic Analysis (PCAP)

```bash
# tshark command line
tshark -r capture.pcap -Y "http" -T fields -e http.host -e http.request.uri | grep flag
tshark -r capture.pcap -Y "http.request.method == POST" -T fields -e http.file_data

# Export HTTP objects
tshark -r capture.pcap -Y "http" --export-objects http,output_dir

# DNS tunnel detection
tshark -r capture.pcap -Y "dns" -T fields -e dns.qry.name | grep -v "^[0-9]"

# Base64 extraction
tshark -r capture.pcap -Y "http" -T fields -e http.file_data | grep -E "^[A-Za-z0-9+/]{20,}={0,2}$"
```

## 4. PDF Steganography

```bash
pdftotext image.pdf -           # Extract text
pdfinfo image.pdf               # Metadata

# Hidden white text: change the background color or simply select all and copy
# Tool: pdf-c11.py
python3 pdf-c11.py image.pdf
```

## 5. Archive Attacks

```bash
# Basic information
zipinfo archive.zip
7z l archive.zip

# Plaintext attack (some known content)
bkcrack -C archive.zip -c known.txt -k XXXXXXXX -r 0/

# Brute force
fcrackzip -v -u -l 1-6 -p passwords.txt archive.zip
fcrackzip -v -u -D -p rockyou.txt archive.zip

# CRC32 attack (small files, 4 bytes of plaintext)
python3 crc_attack.py
```

## 6. Memory Forensics

```bash
volatility -f memory.dmp imageinfo
volatility -f memory.dmp --profile=Win7SP1x64 pslist
volatility -f memory.dmp --profile=Win7SP1x64 netscan
volatility -f memory.dmp --profile=Win7SP1x64 hashdump
volatility -f memory.dmp --profile=Win7SP1x64 mimikatz
volatility -f memory.dmp --profile=Win7SP1x64 filescan
volatility -f memory.dmp --profile=Win7SP1x64 dumpfiles -Q 0xXXXX -D output/
```

## 7. Log Analysis

```bash
grep -i "flag\|password\|admin\|error\|fail" access.log

# SQL injection detection
grep -iE "union.*select|concat.*\(|char\(|0x[0-9a-f]" access.log

# XSS detection
grep -iE "<script|javascript:|onerror=" access.log

# Timing analysis
awk '{print $4}' access.log | sort | uniq -c | sort -rn | head -20
```

## 8. CyberChef

**Online**: https://gchq.github.io/CyberChef/

**Common recipes**:
```
Magic                  # Automatically identify the encoding
From Base64            # Base64 decode
XOR ...                # XOR decryption
ROT13                  # Caesar shift
From Hex               # Hex to characters
Gunzip / Inflate       # Decompress
Reverse                # Reverse a string
Find / Replace         # Replace
```
