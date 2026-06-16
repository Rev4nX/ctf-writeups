# boroCTF 2026 — Amazing (REV, 200pts)

**Author:** Franklin  
**Category:** Reverse Engineering  
**Points:** 200

## Description

> Escape is impossible unless you take the right step.

## Files

- `challenge.py`

---

## Solution

### Step 1 — Read the code

The challenge is a 100×100 maze with a moving player. At first glance it looks like you need to navigate to an exit. This is a red herring.

The real logic is in the `hope()` function, which runs after every move:

```python
def hope():
    sequence = b'#\xbb\xca\xa5...'  # ~500 bytes of encrypted data
    mod = (player_pos[0] ^ (player_pos[1] + player_pos[1])) * player_pos[0]
    try:
        bytes = rsa_encrypt(sequence, mod)
        object = marshal.loads(bytes)
        impossible = types.FunctionType(object, globals(), "impossible")
        impossible()
    except Exception:
        pass
```

Key observations:
- `mod` is derived from the player's current `(row, col)` position
- `rsa_encrypt` despite its name is **not RSA** — it's a XOR stream cipher seeded by `mod`
- The result is passed to `marshal.loads` — Python's bytecode deserializer
- If deserialization succeeds, the resulting function is executed

### Step 2 — Understand `rsa_encrypt`

```python
def rsa_encrypt(data, modulus_length):
    result = bytearray()
    state = modulus_length & 0xFFFFFFFF
    for byte in data:
        state = (1103515245 * state + 12345) & 0xFFFFFFFF
        stream_byte = (state >> 16) & 0xFF
        result.append(byte ^ stream_byte)
    return bytes(result)
```

This is a **Linear Congruential Generator (LCG)** — a classic pseudorandom number generator. The formula `state = (1103515245 * state + 12345) & 0xFFFFFFFF` is the exact LCG from glibc (the C standard library). The `mod` value is used as the seed.

Since the seed is deterministic and the grid is only 100×100, there are exactly 10,000 possible values of `mod`. We can try all of them.

### Step 3 — Bruteforce the position

For each possible `(row, col)` in the 100×100 grid:
1. Compute `mod = (row ^ (col + col)) * row`
2. Decrypt `sequence` with `rsa_encrypt(sequence, mod)`
3. Try `marshal.loads` on the result
4. If it returns a `types.CodeType`, inspect its constants for the flag

The flag is stored as a base64 string in `co_consts` — the constants table of the code object.

### Step 4 — Solver

```python
import marshal
import types
import base64

sequence = b'#\xbb\xca\xa5u\xc15Z...'  # full sequence from challenge.py

def rsa_encrypt(data, modulus_length):
    result = bytearray()
    state = modulus_length & 0xFFFFFFFF
    for byte in data:
        state = (1103515245 * state + 12345) & 0xFFFFFFFF
        stream_byte = (state >> 16) & 0xFF
        result.append(byte ^ stream_byte)
    return bytes(result)

for r in range(100):
    for c in range(100):
        mod = (r ^ (c + c)) * r
        try:
            decrypted = rsa_encrypt(sequence, mod)
            obj = marshal.loads(decrypted)
            if not isinstance(obj, types.CodeType):
                continue
            for const in obj.co_consts:
                if isinstance(const, str):
                    try:
                        decoded = base64.b64decode(const).decode()
                        if decoded.startswith('boro'):
                            print(f"Flag at ({r},{c}):", decoded)
                    except Exception:
                        pass
        except Exception:
            pass
```

Output:
```
Flag at (91,68): boroCTF{es4@pe_wA5_1nev!table}
```

---

## Flag

```
boroCTF{es4@pe_wA5_1nev!table}
```

---

## Key takeaways

- The maze is a complete red herring — you never need to move the player
- `rsa_encrypt` is a misleading name for a simple LCG-based XOR stream cipher
- `marshal` is Python's bytecode serializer — if `marshal.loads` succeeds, you have valid Python code
- `co_consts` is the constants table of a Python code object — a good place to look for hidden strings
- LCG with constants `1103515245` and `12345` is the classic glibc `rand()` implementation
