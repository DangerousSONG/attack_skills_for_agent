---
name: firmware-analysis
description: "Firmware security analysis methodology. Covers firmware acquisition (from the device / download / UART / JTAG), firmware unpacking and filesystem extraction (binwalk / firmware-mod-kit), static analysis (hardcoded credentials / encryption keys / backdoors), dynamic analysis (QEMU emulation), vulnerability research, and firmware modification and repacking. Trigger when the Agent needs to analyze embedded device firmware, extract sensitive information from firmware, or perform IoT device security assessments."
zh-signals: "固件安全分析方法论，涵盖固件获取、解包、静态/动态分析与重打包。信号:固件分析,binwalk,qemu,iot,uart,jtag"
when-to-use: >-
  Use when analyzing embedded device firmware, extracting sensitive data from firmware images,
  or performing IoT device security assessments.
metadata:
  tags: "firmware,firmware analysis,binwalk,qemu,iot security,uart,jtag,embedded"
  category: "hardware"
---

# Firmware Security Analysis Methodology

> **Core Flow**: Acquire firmware → Unpack and extract the filesystem → Statically analyze sensitive information → Dynamically emulate and run → Vulnerability research → Modify and repack the firmware

## Further Reading

- Complete technical details and tool references for firmware analysis → [references/firmware-analysis-techniques.md](references/firmware-analysis-techniques.md)

---

## Phase 1: Firmware Acquisition

```
Firmware acquisition decision tree:
├─ Vendor website download (support page / FTP / CDN)
│  └─ Google dork: site:vendor.com filetype:bin OR filetype:img "firmware"
├─ Cloud storage scanning
│  └─ S3Scanner / GrayhatWarfare to search for the vendor name + firmware
├─ Direct extraction from the device
│  ├─ UART serial connection
│  │  ├─ Identify the TX/RX/GND pins (multimeter / logic analyzer)
│  │  └─ picocom -b 115200 /dev/ttyUSB0
│  ├─ JTAG/SWD debug interface
│  │  └─ Connect with OpenOCD and read the flash
│  ├─ SPI Flash chip direct read
│  │  └─ SOIC-8 clip + flashrom
│  └─ eMMC direct read (ISP solder pads)
├─ Man-in-the-middle interception of update packages
│  └─ Set up a proxy to intercept OTA update requests
├─ Mobile app extraction
│  └─ apktool d vendor-app.apk → assets/firmware/
└─ Dump from the bootloader
   └─ U-Boot: md.b / nand read / sf read
```

### Reading Directly from SPI Flash

```bash
# Use a CH341A programmer + SOIC-8 clip
flashrom -p ch341a_spi -r flash.bin

# Verify read consistency (read twice and compare)
flashrom -p ch341a_spi -r flash2.bin
md5sum flash.bin flash2.bin
```

### Getting a Shell over UART

```bash
# Connect to UART (common baud rates: 115200, 9600, 57600)
picocom -b 115200 /dev/ttyUSB0

# If UART only outputs logs (RX is ignored), edit the U-Boot env to force a shell
# 1. dump flash → 2. modify bootargs to add init=/bin/sh → 3. recompute CRC32 → 4. write back
```

### Extracting Firmware from a Mobile App

```bash
apktool d vendor-app.apk -o vendor-app
ls vendor-app/assets/firmware/
# Common paths: assets/fw/, res/raw/, assets/firmware/
```

## Phase 2: Unpacking and Filesystem Extraction

```
Firmware unpacking decision tree:
├─ binwalk automatic extraction (preferred)
│  └─ binwalk -ev firmware.bin
├─ binwalk identifies it but extraction fails
│  ├─ Manual dd carving + the matching decompression tool
│  │  ├─ squashfs → unsquashfs
│  │  ├─ jffs2 → jefferson
│  │  ├─ cramfs → cramfsck
│  │  ├─ cpio → cpio -ivd
│  │  ├─ ubifs → ubireader_extract_images
│  │  └─ yaffs2 → unyaffs
│  └─ firmware-mod-kit assistance
├─ Encrypted firmware
│  ├─ Check entropy: binwalk -E firmware.bin
│  │  ├─ High entropy → possibly encrypted or compressed
│  │  └─ Low entropy → not encrypted
│  ├─ Look for the decryption key (bootloader / older firmware / reverse the crypto logic)
│  └─ Some vendors use AES-CBC + a hardcoded key/IV
└─ Completely unknown format → hexdump the magic bytes
```

### Standard binwalk Flow

```bash
# Initial analysis (no extraction, identification only)
binwalk firmware.bin

# Entropy analysis to determine whether it is encrypted
binwalk -E firmware.bin

# Automatic recursive extraction
binwalk -ev firmware.bin

# Extraction results are usually in the _firmware.bin.extracted/ directory
ls _firmware.bin.extracted/
```

### Manual Filesystem Extraction

```bash
# Find the filesystem offset
binwalk firmware.bin | grep -i "squashfs\|jffs2\|cramfs\|ubifs"

# Carve with dd (example: squashfs at offset 0x1A0094)
dd if=firmware.bin bs=1 skip=$((0x1A0094)) of=rootfs.squashfs

# Decompress squashfs
unsquashfs rootfs.squashfs
ls squashfs-root/

# Decompress jffs2
jefferson rootfs.jffs2 -d jffs2-root

# Decompress cpio
cpio -ivd --no-absolute-filenames -F rootfs.cpio

# Decompress ubifs
ubireader_extract_images -u UBI -s <start_offset> firmware.bin
```

### Basic File Information Gathering

```bash
file firmware.bin
strings -n8 firmware.bin
strings -tx firmware.bin | head -50
hexdump -C -n 512 firmware.bin
fdisk -lu firmware.bin
```

## Phase 3: Static Analysis

```
Static analysis targets:
├─ Hardcoded credentials
│  ├─ /etc/shadow, /etc/passwd
│  ├─ grep -r "password\|passwd\|secret\|key" etc/
│  └─ Default account passwords in configuration files
├─ Cryptographic material
│  ├─ SSL certificates and private keys: etc/ssl/, *.pem, *.key
│  ├─ SSH keys: etc/ssh/ssh_host_*
│  └─ API keys / tokens
├─ Backdoors and debug interfaces
│  ├─ telnetd / dropbear configuration
│  ├─ Hidden CGI endpoints
│  └─ Debug webshells
├─ Network service configuration
│  ├─ Web server configuration (lighttpd/uhttpd/mini_httpd)
│  ├─ MQTT credentials and broker addresses
│  └─ Cloud platform API endpoints
├─ Boot script analysis
│  ├─ /etc/init.d/, /etc/rc.d/
│  └─ Service start order and privileges
└─ Binary security checks
   └─ checksec --file=<binary>
```

### Credential and Sensitive Information Search

```bash
# Enter the extracted filesystem
cd squashfs-root/

# Check user credentials
cat etc/shadow 2>/dev/null
cat etc/passwd

# Search for hardcoded passwords
grep -rn "password\|passwd\|secret\|api_key\|token" etc/ --include="*.conf" --include="*.cfg"
grep -rn "password\|passwd" usr/lib/ --include="*.lua" --include="*.sh"

# Search for SSL/SSH keys
find . -name "*.pem" -o -name "*.key" -o -name "*.crt" -o -name "ssh_host_*"

# Search for URLs and IP addresses
grep -rn "http://\|https://\|ftp://" . --include="*.conf" --include="*.sh" --include="*.lua"
grep -rEn "\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\b" etc/

# Search for base64-encoded content (may hide credentials)
grep -rn "^[A-Za-z0-9+/=]\{20,\}$" etc/
```

### Automated Analysis Tools

```bash
# Firmwalker - automatic sensitive information search
./firmwalker.sh squashfs-root/

# EMBA - comprehensive firmware security analysis
sudo ./emba -f firmware.bin -l ./logs

# LinPEAS (run inside the emulated environment)
# Copy it into the emulated filesystem and execute it
```

### Binary Protection Checks

```bash
# Check the secure compilation options of all ELF binaries
find squashfs-root/ -executable -type f -exec file {} \; | grep ELF
checksec --file=squashfs-root/usr/bin/httpd
checksec --file=squashfs-root/usr/sbin/dropbear
```

### Cloud Credential and MQTT Configuration Extraction

```bash
# Search for MQTT configuration
grep -rn "mqtt\|broker\|mosquitto" etc/ usr/ --include="*.conf" --include="*.json"

# Search for cloud endpoint URLs and token derivation logic
grep -rn "/pf/\|deviceId\|STATIC_KEY" usr/bin/ usr/lib/
strings usr/bin/cloud_agent | grep -i "mqtt\|api\|token\|key\|secret"
```

## Phase 4: Dynamic Analysis (QEMU Emulation)

```
Dynamic analysis decision tree:
├─ Emulating a single binary
│  ├─ Confirm the architecture: file <binary>
│  ├─ MIPS big-endian → qemu-mips
│  ├─ MIPS little-endian → qemu-mipsel
│  ├─ ARM → qemu-arm
│  ├─ ARM64 → qemu-aarch64
│  └─ Requires chroot or --root pointing at the filesystem
├─ Full system emulation
│  ├─ Firmadyne (automated, recommended)
│  ├─ Firmware Analysis Toolkit (based on Firmadyne)
│  └─ Manual QEMU system emulation
└─ Dynamic debugging on the real device
   ├─ gdbserver remote debugging
   └─ Frida hook
```

### Emulating a Single Binary

```bash
# Install the QEMU user-mode emulator
sudo apt-get install qemu-user-static

# Confirm the target architecture
file squashfs-root/bin/busybox

# MIPS emulation (using the extracted filesystem as root)
sudo chroot squashfs-root /usr/bin/qemu-mips-static /bin/busybox ls

# ARM emulation
sudo chroot squashfs-root /usr/bin/qemu-arm-static /usr/sbin/httpd

# Emulation with strace (to observe system calls)
qemu-mips-static -strace ./squashfs-root/usr/bin/target_binary
```

### Full System Emulation (Firmadyne)

```bash
# Firmadyne flow
# 1. Extract the firmware filesystem
python3 ./sources/extractor/extractor.py -b <brand> -sql <psql_ip> -np -nk firmware.bin images/

# 2. Identify the architecture
python3 ./scripts/getArch.sh images/<image_id>.tar.gz

# 3. Create the QEMU image
python3 ./scripts/makeImage.sh <image_id>

# 4. Infer the network configuration
python3 ./scripts/inferNetwork.sh <image_id>

# 5. Start the emulation
python3 ./scratch/<image_id>/run.sh
```

### Remote Debugging

```bash
# Start gdbserver on the device / in the emulated environment
gdbserver :1234 /usr/bin/target_daemon

# Connect from the host
gdb-multiarch /path/to/target_daemon
# (gdb) target remote <device-ip>:1234
# (gdb) set architecture mips
# (gdb) continue
```

## Phase 5: Vulnerability Research

```
Common firmware vulnerability types:
├─ Command injection
│  ├─ Web CGI parameters not filtered
│  ├─ System calls built by concatenating user input
│  └─ grep -rn "system\|popen\|exec\|eval" --include="*.c" --include="*.lua"
├─ Buffer overflow
│  ├─ Unsafe functions such as strcpy/sprintf/gets
│  ├─ Embedded systems usually lack protections (no ASLR/NX/Canary)
│  └─ Use checksec to confirm the protection status
├─ Authentication bypass
│  ├─ Hardcoded credentials
│  ├─ Backdoor accounts
│  └─ session management flaws
├─ Information disclosure
│  ├─ Unauthenticated API endpoints
│  ├─ Debug information exposure
│  └─ Accessible configuration files
├─ Downgrade attacks
│  ├─ Signed update mechanisms without version checks
│  ├─ Older signed firmware can still be flashed
│  └─ Security patch bypass
├─ MQTT/cloud credential leak
│  ├─ Tokens derived from a hardcoded STATIC_KEY
│  ├─ Plaintext MQTT credentials
│  └─ Weak topic ACLs allow cross-device access
└─ uClibc heap exploitation (specific to embedded Linux)
   ├─ Fake chunk during fastbin consolidation
   ├─ Stable .data/.bss addresses without PIE
   └─ Write shellcode via /proc/self/mem
```

### Web Service Vulnerability Testing

```bash
# Identify the web service
nmap -sV -p 80,443,8080,8443 <device-ip>

# Collect all CGI endpoints
curl -s http://<device-ip>/ | grep -oP 'action="[^"]*"|href="[^"]*"'
find squashfs-root/www/ -name "*.cgi" -o -name "*.asp" -o -name "*.lua"

# Command injection test (targeted testing after static analysis)
# Analyze the source of the arguments passed to system() in the CGI binary
strings squashfs-root/usr/bin/httpd | grep "system\|popen\|/bin/sh"
```

### Update Mechanism Audit

```bash
# Check the update logic: is the version number verified?
strings squashfs-root/usr/bin/upgrade_manager | grep -i "version\|rollback\|verify\|sign"

# Is there an anti-downgrade counter?
grep -rn "anti.rollback\|version.check\|monotonic" squashfs-root/etc/ squashfs-root/usr/
```

## Phase 6: Firmware Modification and Repacking

```
Firmware modification flow:
├─ Modify the filesystem contents
│  ├─ Add an SSH public key to /root/.ssh/authorized_keys
│  ├─ Modify /etc/shadow (add a user with a known password)
│  ├─ Implant a reverse shell or busybox
│  └─ Modify the boot script to add a persistence backdoor
├─ Repack the filesystem
│  ├─ squashfs: mksquashfs <dir> rootfs.squashfs -comp xz
│  ├─ jffs2: mkfs.jffs2 -d <dir> -o rootfs.jffs2
│  └─ cramfs: mkcramfs <dir> rootfs.cramfs
├─ Reassemble the firmware image
│  ├─ Concatenate the partitions with dd
│  ├─ firmware-mod-kit automatic repacking
│  └─ Update the CRC/checksum (if present)
└─ Flash onto the device
   ├─ Upload through the Web UI
   ├─ TFTP / serial flashing
   └─ Direct SPI write with flashrom
```

### Repacking Example

```bash
# Repack squashfs after modifying the filesystem
# Note: match the original compression algorithm and block size
mksquashfs squashfs-root/ new_rootfs.squashfs -comp xz -b 131072

# Repack with firmware-mod-kit
./build-firmware.sh <extraction_dir>

# Manually assemble the firmware
dd if=header.bin of=modified_firmware.bin bs=1
dd if=new_rootfs.squashfs of=modified_firmware.bin bs=1 seek=<offset> conv=notrunc

# Recompute the CRC (if the firmware header contains a checksum)
# Reverse engineer the firmware header format to determine the CRC algorithm and its location
```

## Tool Quick Reference

| Tool | Purpose |
|------|------|
| binwalk | Firmware identification and extraction |
| firmware-mod-kit | Unpacking / repacking |
| flashrom | SPI Flash read/write |
| OpenOCD | JTAG debugging |
| QEMU | Binary / system emulation |
| Firmadyne | Automated full system emulation |
| Ghidra / radare2 | Binary reverse engineering |
| gdbserver + gdb-multiarch | Remote debugging |
| checksec | Binary protection checks |
| EMBA | Comprehensive firmware security analysis |
| Firmwalker | Sensitive information search |
| picocom / minicom | Serial communication |

## Practice Lab Range

| Item | Description |
|------|------|
| OWASP IoTGoat | IoT firmware vulnerability practice |
| DVRF | Damn Vulnerable Router Firmware |
| DVAR | Damn Vulnerable ARM Router |
| ARM-X | ARM firmware emulation framework |
| DVID | Damn Vulnerable IoT Device |
