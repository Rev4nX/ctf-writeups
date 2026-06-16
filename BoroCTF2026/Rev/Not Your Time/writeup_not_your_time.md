# boroCTF 2026 — Not Your Time (Rev, 100pts)

**Author:** Franklin  
**Category:** Rev  

## Description

> One of the trifecta of bitwise operations.

## Files

- `chal` (ELF 64-bit executable)

---

## Solution

### Step 1 — Identify the binary

```bash
file chal
# ELF 64-bit LSB pie executable, x86-64, dynamically linked, stripped
```

Load into Ghidra and decompile `main`.

### Step 2 — Analyze the decompiled code

After renaming variables in Ghidra, the logic is clear:

```c
bool main(void)
{
  bool match;
  long in_FS_OFFSET;
  int i;
  uint encoded_flag [28];
  char input [40];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);  // stack canary
  encoded_flag[0] = 0x9d;
  encoded_flag[1] = 0x90;
  encoded_flag[2] = 0x8d;
  // ... 25 hardcoded values total
  encoded_flag[0x18] = 0x82;

  printf("> ");
  __isoc99_scanf(&DAT_00102007, input);

  match = true;
  for (i = 0; i < 25; i = i + 1) {
    if ((int)input[i] != (~encoded_flag[i] & 0xff)) {
      match = false;
    }
  }
  // ...
}
```

The key line: `input[i] != (~encoded_flag[i] & 0xff)`

The operation is **bitwise NOT** (`~`) — one of the classic bitwise trio (AND, OR, XOR). NOT is technically unary (one operand), but it's equivalent to XOR with `0xFF`, which flips all 8 bits. That's why the description says "one of the trifecta" — NOT is just XOR with all ones.

### Step 3 — Why the & 0xFF is in the C code

The array is declared as `uint` (32-bit unsigned int), not `uint8_t` (8-bit). When you apply `~` to a 32-bit value, it flips **all 32 bits** — the upper 24 bits get set to 1 as well, producing a large number like `0xFFFFFF62` instead of the intended `0x62`.

The `& 0xFF` masks off the upper 24 bits, keeping only the last 8. This is a C type safety measure, not part of the encoding logic — if the array had been declared as `uint8_t`, the `& 0xFF` would not be needed at all.

In the Python solver, this is not an issue — all values are already in the 0–255 range, so `^ 0xFF` is sufficient without any masking.

### Step 4 — Python pitfall: ~ behaves differently

In Python, `~x` returns a negative number (e.g. `~0x9d` = `-0x9e`) because Python integers have arbitrary precision. Using `x ^ 0xFF` avoids this entirely and is the cleanest approach:

```python
0x9d ^ 0xFF  # = 0x62 ✓
```

### Step 5 — Solver

Copy the hardcoded values from Ghidra into `data.txt`, one assignment per line:

```
encoded_flag[0] = 0x9d;
encoded_flag[1] = 0x90;
...
```

```python
def parse_value(line):
    if "=" not in line:
        return None
    raw = line.split("=")[1].strip().rstrip(";")
    return int(raw, 16) if raw.startswith("0x") else int(raw)

def transform(x):
    return x ^ 0xFF

with open("data.txt") as f:
    for line in f:
        v = parse_value(line)
        if v is not None:
            print(chr(transform(v)), end="")
```

Output: `boroCTF{N0t_nO+_tH3_FL@g}`

---

## Flag

```
boroCTF{N0t_nO+_tH3_FL@g}
```

---

## Key takeaways

- NOT is technically unary (not one of the binary trio AND/OR/XOR), but it equals XOR with `0xFF` — flipping all bits. That's the connection the description hints at
- The `& 0xFF` in the C code is **not part of the encoding** — it's a type safety mask because the array is declared as `uint` (32-bit). After `~`, the upper 24 bits would be set to 1, producing e.g. `0xFFFFFF62` instead of `0x62`. The mask zeroes those out. With `uint8_t`, it wouldn't appear at all
- AND = bitwise multiplication, XOR = bitwise addition mod 2, OR has no clean arithmetic analogy — it "saturates": once a bit is set to 1 via OR, it stays 1
- In Python, never use `~x` directly — use `x ^ 0xFF` instead, which avoids the negative number issue entirely
- Rename variables in Ghidra as you go — it makes the logic immediately readable
- The `parse_value` + `transform` solver template is reusable: next challenge, just change what `transform` does
