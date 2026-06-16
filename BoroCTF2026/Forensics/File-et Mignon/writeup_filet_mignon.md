# boroCTF 2026 — File-et Mignon (Forensics, 200pts)

**Author:** ForeverFlames  
**Category:** Forensics  

## Description

> Don't try to bite off more than you can chew.

## Files

- `filet_mignon_challenge.tar.gz`

---

## Solution

### Step 1 — Download correctly

Downloading via browser results in a 0-byte file — the browser fails silently when handling the archive. Use `curl` instead:

```bash
curl "https://boroctf.com/files/.../filet_mignon_challenge.tar.gz?token=..." -o filet_mignon_challenge.tar.gz
```

This gives a proper 344-byte archive.

### Step 2 — Extract

```bash
tar -xzf filet_mignon_challenge.tar.gz
ls -la
```

Output: `filet_mignon.bin` with a logical size of **~11 TB** but actual disk usage of only **32 KB**.

### Step 3 — Understand the sparse file

`filet_mignon.bin` is a **sparse file** — a filesystem feature where a file can have a huge logical size but only the blocks containing actual non-zero data are physically stored. The rest are "holes" filled with virtual zeros that take no disk space.

The hint "don't bite off more than you can chew" means: don't try to read 11 TB naively — `cat`, `xxd`, or loading it into memory will hang or crash your machine.

### Step 4 — Find the data regions

Linux provides `SEEK_DATA` and `SEEK_HOLE` — special seek modes that jump directly to the next data region or hole without reading the zeros in between:

```python
import os

SEEK_DATA = 3
SEEK_HOLE = 4

f = os.open('filet_mignon.bin', os.O_RDONLY)
size = os.fstat(f).st_size
print(f'Logical size: {size:,} bytes ({size/1e12:.1f} TB)')

offset = 0
flag = ''
while offset < size:
    try:
        data_start = os.lseek(f, offset, SEEK_DATA)
    except OSError:
        break
    if data_start >= size:
        break
    try:
        hole_start = os.lseek(f, data_start, SEEK_HOLE)
    except OSError:
        hole_start = size
    os.lseek(f, data_start, 0)
    data = os.read(f, hole_start - data_start)
    printable = bytes(b for b in data if 32 <= b < 127).decode()
    flag += printable
    offset = hole_start

print('Flag:', flag)
os.close(f)
```

Output: 8 data regions at 1 TB intervals, each containing 5 characters of the flag.

---

## Flag

```
boroCTF{y0u_c4rv3d_th3_v01d_l1k3_4_ch3f}
```

---

## Key takeaways

- **Sparse files** have huge logical size but tiny actual disk usage — always check `du -h` vs `ls -la` to spot the difference
- `SEEK_DATA` / `SEEK_HOLE` let you navigate sparse files efficiently without reading terabytes of zeros
- "Don't bite off more than you can chew" = don't read the whole file naively
- **Browser vs curl:** the browser failed to download the file correctly (0 bytes). When a file seems empty, try `curl` — it downloads raw bytes without any processing
- **Work in WSL home directory, not on Windows:** extracting sparse files to `/mnt/c/` (Windows NTFS) fails with I/O errors because NTFS does not support sparse files the same way ext4 does. Always extract to `~/` (i.e. `/home/username/`) which is on the Linux ext4 filesystem
- **Never trust an LLM to assemble a flag for you.** In this challenge, the script correctly read byte `0x31` (digit `1`) from the file, but when composing the flag as text, the LLM wrote `v0id` instead of `v01d` — because `void` is a common English word and LLMs predict the most probable token sequence, not the most accurate one. The data was correct; the LLM's text generation was not. The fix: always run the code yourself locally and copy the output directly — never let an LLM transcribe raw bytes into text by hand. This is especially dangerous with leet speak where `1`/`l`/`i` and `0`/`O` are visually similar even for humans, and an LLM adds an extra layer of risk by drifting toward real words.
