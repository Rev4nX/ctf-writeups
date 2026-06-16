# boroCTF 2026 — Flipper's Dilemma (Crypto, 100pts)

**Author:** Franklin  
**Category:** Crypto  

## Description

> Why do we flip a coin when we have to make a hard choice? Maybe the flipping here isn't so random. I flipped it once yet still 0x15 times.
> `wzgzVASnS4|eE${J%`>h`

---

## Solution

### Step 1 — Read the hint

Two signals in the description:
- "flipped" → XOR (bit flip operation)
- "0x15 times" → the key is `0x15`

Bonus insight: "flipped once yet still 0x15 times" — XOR is self-inverse, so applying it an odd number of times gives the same result as applying it once. XOR 21 times = XOR 1 time (21 is odd). The hint confirms the key is `0x15 = 21`.

### Step 2 — XOR each byte with 0x15

```python
ciphertext = 'wzgzVASnS4|eE${J%`>h'
result = ''.join(chr(ord(c) ^ 0x15) for c in ciphertext)
print(result)
```

Output: `boroCTF{F!ipP1n_0u+}`

---

## Flag

```
boroCTF{F!ipP1n_0u+}
```

---

## Key takeaways

- XOR with any value is a "bit flip" — XOR with `0xFF` flips all 8 bits (bitwise NOT), XOR with `0x15` flips only the bits where `0x15` has a `1` (bits 0, 2, 4)
- XOR is self-inverse: `x ^ k ^ k = x`. Applying the same XOR an even number of times cancels out; odd number of times = same as once
- When you see a hex value in the hint, try it as an XOR key first
- CyberChef: XOR operation with key `15` (hex) solves this in one click
