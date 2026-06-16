# boroCTF 2026 — Hidden but definitely not (REV, 100pts)

**Author:** Franklin  
**Category:** Reverse Engineering  
**Points:** 100  
**Solves:** 278

## Description

> The most trite challenge concept.

## Files

- `password_protected`

---

## Solution

### Step 1 — Identify the file type

```bash
file password_protected
# password_protected: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV),
# dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2,
# BuildID[sha1]=22484cb1eb941eb87482b6d24060bb6edce1d795,
# for GNU/Linux 3.2.0, stripped
```

64-bit Linux ELF, stripped (no debug symbols).

### Step 2 — Load into Ghidra

Import the binary into Ghidra and run auto-analysis. Open the `main` function in the decompiler.

### Step 3 — Analyze the decompiled code

The decompiled `main` function reveals two distinct parts:

**Part 1 — Password verification (noise):**

```c
char expected_password[8];
char password_input[128];

builtin_strncpy(expected_password, "Rate5Sta", 8);
// ... more string building via strncpy and hex literals ...

fgets(password_input, 128, stdin);
size_t len = strcspn(password_input, "\n");
password_input[len] = '\0';

int cmp_result = strcmp(password_input, expected_password);
if (cmp_result == 0) {
    // decode and print flag
}
```

The program builds a password from hardcoded fragments and compares it to user input. This is intentionally convoluted to distract from the actual flag mechanism.

**Part 2 — Flag decoding (the actual target):**

```c
encoded_flag[0]  = 0x65;
encoded_flag[1]  = 0x68;
// ... 34 bytes total ...
encoded_flag[0x21] = 0x7a;

// XOR loop
int i = 0;
while (true) {
    size_t len = strlen((char *)encoded_flag);
    if (len <= (unsigned long)(long)i) break;
    putchar((int)(char)(encoded_flag[i] ^ 7));
    i++;
}
putchar(10);
```

Each byte of `encoded_flag` is XORed with `7` and printed. The flag is fully static — it does not depend on the password input at all.

### Step 4 — Write a solver

Extract all byte values from Ghidra and decode them with Python:

```python
import re

# Paste the encoded_flag assignments from Ghidra here
dump = """
encoded_flag[0] = 0x65;
encoded_flag[1] = 0x68;
encoded_flag[2] = 0x75;
encoded_flag[3] = 0x68;
encoded_flag[4] = 0x44;
encoded_flag[5] = 0x53;
encoded_flag[6] = 0x41;
encoded_flag[7] = 0x7c;
encoded_flag[8] = 0x4e;
encoded_flag[9] = 0x58;
encoded_flag[10] = 0x4f;
encoded_flag[0xb] = 0x3f;
encoded_flag[0xc] = 0x58;
encoded_flag[0xd] = 0x4a;
encoded_flag[0xe] = 0x47;
encoded_flag[0xf] = 0x30;
encoded_flag[0x10] = 0x6e;
encoded_flag[0x11] = 0x69;
encoded_flag[0x12] = 0x60;
encoded_flag[0x13] = 0x58;
encoded_flag[0x14] = 0x54;
encoded_flag[0x15] = 0x73;
encoded_flag[0x16] = 0x55;
encoded_flag[0x17] = 0x36;
encoded_flag[0x18] = 0x69;
encoded_flag[0x19] = 0x60;
encoded_flag[0x1a] = 0x32;
encoded_flag[0x1b] = 0x58;
encoded_flag[0x1c] = 100;
encoded_flag[0x1d] = 0x4f;
encoded_flag[0x1e] = 0x66;
encoded_flag[0x1f] = 0x6b;
encoded_flag[0x20] = 0x74;
encoded_flag[0x21] = 0x7a;
"""

matches = re.findall(r'\[([^\]]+)\] = (0x[0-9a-f]+|\d+);', dump)
data = {}
for idx, val in matches:
    i = int(idx, 16) if idx.startswith('0x') else int(idx)
    v = int(val, 16) if val.startswith('0x') else int(val)
    data[i] = v

print(''.join(chr(data[i] ^ 7) for i in sorted(data)))
```

The regex extracts both hex and decimal indices, stores them in a dictionary keyed by index, sorts them, and applies XOR 7 — replicating exactly what the binary does at runtime.

---

## Flag

```
boroCTF{I_H8_M@7ing_StR1ng5_cHals}
```

---

## Key takeaways

- The password mechanism is a red herring — the flag is stored statically in `encoded_flag` and decoded via XOR regardless of user input
- Always look at the full function before spending time on any one part
- Indices in Ghidra output can be hex or decimal — parse both when writing solvers
- Replicating the binary's own decoding logic in Python is often faster than figuring out the correct runtime input
