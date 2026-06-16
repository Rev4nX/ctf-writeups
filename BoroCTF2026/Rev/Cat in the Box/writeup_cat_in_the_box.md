# boroCTF 2026 — Cat in the ...Box? (Rev, 200pts)

**Author:** Franklin  
**Category:** Rev  

## Description

> We love cats over here at boroCTF. We feel like we have a hidden connection to them.

## Files

- `cat` (ELF 64-bit executable, stripped)

---

## Solution

### Step 1 — Initial recon

```bash
file cat
# ELF 64-bit LSB pie executable, x86-64, dynamically linked, stripped
```

Load into Ghidra. First step: `Search → For Strings` to get an immediate map of the binary's constants.

Key finds:
- `curl -s -o "%s" "%s%s%s"` — the program downloads something from the internet
- 50 password strings: `a1b2c3`, `x7y8z9`, `q1w2e3`... `ymweyc`... `golden`, `silver`
- `Binary no reponse. Try again in a moment.` — error message
- Two encrypted blobs at `DAT_00102010` (25 bytes) and `DAT_00102029` (4 bytes)

This tells us: flag is on an external server, fetched via `curl`.

### Step 2 — Analyze `logic` function

> Note: variable names have been renamed from Ghidra's defaults for readability.

```c
undefined8 logic(undefined8 param_1, sockaddr *param_2)
{
    uint i = 0;
    while ((((int)i < 0 || ((int)i % 14 != 1)) || ((int)i % 3 != 2))) {
        i = i + 1;
        if (49 < i) goto LAB_fetch;
    }
    iVar1 = connect((&PTR_s_a1b2c3_00104020)[(int)i], param_2, i * 8);
    // ...
LAB_fetch:
    uVar2 = read_two_lines(local_10);
    printf("%s", uVar2);
    return 0;
}
```

The loop searches for `i` satisfying both:
- `i % 14 == 1`
- `i % 3 == 2`

Brute forcing 0–49: **i = 29**.

`PTR_s_a1b2c3_00104020` is a table of 50 pointers to the password strings. Index `[29]` points to address `0x001020f8`.

### Step 3 — Find the key

Navigate to `0x001020f8` in Ghidra listing: `s_ymweyc_001020f8` — the string is **`ymweyc`**.

This is the XOR key and simultaneously the middle part of the URL.

### Step 4 — Analyze the `connect` function (custom, not libc)

The author named their function `connect` to shadow the libc syscall — a classic anti-RE trick.

```c
// Decode URL prefix: 25 bytes from DAT_00102010 XOR key
for (i = 0; i < 0x19; i++) {
    local_228[i] = DAT_00102010[i] ^ key[i % strlen(key)];
}
// Decode URL suffix: 4 bytes from DAT_00102029 XOR key
for (i = 0; i < 4; i++) {
    local_1a8[i] = DAT_00102029[i] ^ key[i % strlen(key)];
}
// Build and execute curl command
snprintf(cmd, 0x100, "curl -s -o \"%s\" \"%s%s%s\"",
         tmpfile, prefix, key, suffix);
system(cmd);
```

URL structure: `prefix + key + suffix`

### Step 5 — Decode the URL

Raw bytes from `.rodata`:
- `DAT_00102010` (25 bytes): `11 19 03 15 0a 59 56 42 11 0c 15 06 0a 43 14 04 0d 01 16 15 59 08 16 06 56`
- `DAT_00102029` (4 bytes): `57 19 0f 11`
- Key: `ymweyc`

```python
key = b'ymweyc'

prefix_enc = bytes.fromhex('111903150a595642110c15060a4314040d011615590816 0656'.replace(' ', ''))
suffix_enc = bytes.fromhex('57190f11')

prefix = bytes([b ^ key[i % len(key)] for i, b in enumerate(prefix_enc)])
suffix = bytes([b ^ key[i % len(key)] for i, b in enumerate(suffix_enc)])

print(f'{prefix.decode()}{key.decode()}{suffix.decode()}')
# https://files.catbox.moe/ymweyc.txt
```

### Step 6 — Fetch the flag

```bash
curl -s "https://files.catbox.moe/ymweyc.txt"
```

Response:
```
The cat wispers the flag to you ...
Segmentation fault (core dumped)
-----------------
SUPER SECRET AREA
-----------------
Yeah, I hardcoded the segfault.
Here's your real flag: boroCTF{lEts_gO_B3y0nd_b1nar1e$}
```

Note: the "Segmentation fault" is a joke — it's just text in the server response, not a real crash.

---

## Flag

```
boroCTF{lEts_gO_B3y0nd_b1nar1e$}
```

---

## Key takeaways

- **`Search → For Strings` first** — `curl -s -o "%s" "%s%s%s"` immediately revealed the program fetches content from the internet. Always run this before diving into the decompiler
- **Shadowing libc functions** — the author named their custom function `connect` to shadow the real libc `connect` syscall. A classic anti-RE trick; check imports vs. local functions carefully
- **Key serves double duty** — `ymweyc` is both the XOR decryption key for the URL fragments AND the middle segment of the URL itself. Elegant design
- **`i % 14 == 1` AND `i % 3 == 2`** — the Schrödinger reference: the "correct state" only exists at one specific index (29) found by solving simultaneous modular conditions. The cat is only "observed" at this one point
- **`.rodata` layout** — encrypted blobs sit before the plaintext password table in `.rodata`. The blobs are invisible to `strings` but the password table is fully readable — which is intentional misdirection (you see `a1b2c3` first and assume that's the key)
- **Stripped binary** — strip removes local variable names and debug symbols, but NOT imported library function names (resolved at link time). Ghidra identifies them from the dynamic symbol table
