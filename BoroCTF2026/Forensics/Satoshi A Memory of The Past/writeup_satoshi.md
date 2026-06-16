# boroCTF 2026 — Satoshi: A Memory of The Past (Forensics, 100pts)

**Author:** ForeverFlames  
**Category:** Forensics (actually RE-level difficulty)

## Description

> All these crimes. Its not him. His soul is gone. It took his soul and trapped it inside the cache. I still hear his pulse.... Please don't lose his memory. I can't live without my beloved Satoshi.  
> Satoshi's wife, Yukiko Nakamuda  
> (Note: the flag is already wrapped in boroCTF{} when you find it)

## Files

- `Forgotten.zip` → `satoshi_pulse_v2` (ELF 64-bit)

---

## Solution

### Step 1 — Identify the binary

```bash
file satoshi_pulse_v2
chmod +x satoshi_pulse_v2
./satoshi_pulse_v2
```

Output: Japanese text "私はまだここにいます... (I am still here...)", then a stream of large numbers like `576`, `7168`, `192`, `8224`...

### Step 2 — Load into Ghidra

Open `satoshi_pulse_v2` in Ghidra, analyze, open `main` in the decompiler.

The decompiler may show garbled output with `&stack0xffffffffffdfff68` references instead of concrete values — the bytes haven't been disassembled yet.

**Fix:** In the Listing (ASM) view, navigate to address `0010122d`, press `D` (disassemble). Ghidra will reinterpret the bytes as instructions and the decompiler will update to show concrete values.

### Step 3 — Understand the code

After disassembly, the decompiler shows:

```c
*(undefined4 *)(unaff_RBP + -0x200090) = 0x20;
*(undefined4 *)(unaff_RBP + -0x20008c) = 0x2d;
...
*(undefined4 *)(unaff_RBP + -0x200020) = 0x3f;
*(undefined4 *)(unaff_RBP + -0x2000b4) = 0x1d;  // counter = 29
```

29 values are written to the stack. The outer loop processes `0x1d` (29) bytes:

```c
*(byte *)(...) = (byte)*(array + byte_idx*4) ^ 0x42;  // XOR decode
```

For each decoded byte, the inner loop iterates over 8 bits. Each bit either:
- **bit=1**: calls `clflush` (flush cache line) → slow memory access → large rdtsc delta
- **bit=0**: no flush → fast access → small rdtsc delta

Then `printf("%llu\n")` prints the timing delta. This is a **Flush+Reload cache side-channel** — the flag is "transmitted" as timing differences rather than printed directly.

`demonic_logic()` is a red herring — it just wastes CPU cycles to make timing differences measurable.

### Step 4 — Extract the flag statically

We don't need to run the side-channel. The 29 encoded values are hardcoded in the binary. XOR each with `0x42`:

```python
vals = [
    0x20, 0x2d, 0x30, 0x2d, 0x01, 0x16, 0x04, 0x39,
    0x31, 0x76, 0x36, 0x72, 0x31, 0x2a, 0x73, 0x1d,
    0x73, 0x2c, 0x1d, 0x36, 0x2a, 0x71, 0x1d, 0x21,
    0x76, 0x21, 0x2a, 0x71, 0x3f
]
print(''.join(chr(v ^ 0x42) for v in vals))
```

Or parse directly from a Ghidra decompiler dump saved to `data.txt`:

```python
with open("data.txt") as file:
    for line in file:
        raw = line.split("=")[1].strip().rstrip(";")

        if raw.startswith("0x"):
            value = int(raw, 16)
        else:
            value = int(raw)

        flag_piece = value ^ 0x42
        character = chr(flag_piece)
        print(character, end="")
```

Output: `boroCTF{s4t0sh1_1n_th3_c4ch3}`

---

## Flag

```
boroCTF{s4t0sh1_1n_th3_c4ch3}
```

---

## Key takeaways

- **Flush+Reload** is a real CPU cache side-channel attack — used in Spectre/Meltdown. Here it's used to encode flag bits as timing differences (slow = bit 1, fast = bit 0)
- `demonic_logic()` is a red herring — it just burns CPU cycles. Always check if a function affects the output before analyzing it deeply
- **Static analysis beats dynamic** here — the encoded values were hardcoded in the binary, so running the side-channel wasn't needed at all
- **When Ghidra's decompiler shows garbled output**, go to the Listing (ASM) view, navigate to the problematic address, press `D` to disassemble — the decompiler will update
- **Follow variables from the decompiler** to find where data is initialized — click on a variable name and Ghidra highlights its usages
- Parsing Ghidra decompiler output with Python (`split("=")`, `strip()`, `rstrip(";")`, `int(x, 16)`) is a reusable pattern for extracting hardcoded arrays
