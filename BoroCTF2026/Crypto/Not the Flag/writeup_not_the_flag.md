# boroCTF 2026 — Not the Flag (Crypto, 100pts)

**Author:** ForeverFlames  
**Category:** Crypto  

## Description

> So is this not the flag? If its not not, then what else?  
> `9d 90 8d 90 bc ab b9 84 8b 97 ce db a0 96 8c a0 91 cf 8b a0 91 90 8b a0 8b 97 cc a0 99 93 bf 98 82`

---

## Solution

### Step 1 — Read the hint

"If it's not not" — double negation. One "not" is English negation, the other is the **bitwise NOT operator**. Double negation = apply NOT to get back the original = the data has been bitwise-NOT'd, so we need to NOT it again.

### Step 2 — Understand XOR 0xFF = bitwise NOT

XOR with `0xFF` (`11111111` in binary) flips every bit — this is equivalent to bitwise NOT.

Example:
```
9d = 10011101
FF = 11111111
XOR= 01100010 = 62 = 'b'
```

### Step 3 — Decode

```python
data = [0x9d, 0x90, 0x8d, 0x90, 0xbc, 0xab, 0xb9, 0x84, 0x8b, 0x97, 0xce, 0xdb,
        0xa0, 0x96, 0x8c, 0xa0, 0x91, 0xcf, 0x8b, 0xa0, 0x91, 0x90, 0x8b, 0xa0,
        0x8b, 0x97, 0xcc, 0xa0, 0x99, 0x93, 0xbf, 0x98, 0x82]

result = bytes([b ^ 0xFF for b in data])
print(result.decode())
```

Output: `boroCTF{th1$_is_n0t_not_th3_fl@g}`

---

## Flag

```
boroCTF{th1$_is_n0t_not_th3_fl@g}
```

---

## Key takeaways

- "not not" in the description = double negation = bitwise NOT hint
- XOR 0xFF = bitwise NOT = flips every bit (since `0xFF` = `11111111`)
- XOR 0x00 would do nothing (any value XOR 0 = same value) — useless as encryption
- When you have raw bytes with no key, try XOR 0xFF as the first move
- `bytes([...])` stores values as a contiguous sequence with no separators — `.decode()` then interprets each byte as an ASCII character
