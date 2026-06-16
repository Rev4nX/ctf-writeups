# boroCTF 2026 — So Many Layers (Crypto, 100pts)

**Author:** Franklin  
**Category:** Crypto  

## Description

> Makes me cry.
> `00110101 00111001 00110110 01000100 00110011 00111001 00110111 00111001 00110110 00110010 00110011 00110000 00110100 01000101 00110101 00110101 00110101 00110010 00110110 01000101 00110111 00110100 00110100 01000100 00110100 00111001 00110101 00110111 00110111 00110011 00110111 01000001 00110101 00111000 00110011 00110010 00110100 00110110 00110100 01000110 00110101 00111000 00110111 01000001 00110100 00110010 00110111 00110101 00110100 01000100 00110101 00110111 00110011 00111001 00110111 00110101 00110101 00111000 00110110 01000101 00110011 00110000 00110011 01000100`

---

## Solution

The title "So Many Layers" and "makes me cry" hint at an onion — multiple layers of encoding to peel, and onions make you cry.

### Layer 1 — Binary → ASCII hex

Each group of 8 bits is one ASCII character:

```python
binary = '00110101 00111001 ...'
layer1 = ''.join(chr(int(b, 2)) for b in binary.split())
# 596D397962304E55526E744D4957737A5832464F587A42754D573975586E303D
```

Result looks like hex — only characters `0-9` and `A-F`, even length.

### Layer 2 — Hex → ASCII base64

```python
import binascii
layer2 = bytes.fromhex(layer1).decode()
# Ym9yb0NURntMIWszX2FOXzBuMW9uXn0=
```

Result ends with `=` and contains only alphanumeric + `+/` — recognizable base64.

### Layer 3 — Base64 → plaintext

```python
import base64
layer3 = base64.b64decode(layer2).decode()
# boroCTF{L!k3_aN_0n1on^}
```

### Full solver

```python
import base64

binary = '00110101 00111001 00110110 01000100 00110011 00111001 00110111 00111001 00110110 00110010 00110011 00110000 00110100 01000101 00110101 00110101 00110101 00110010 00110110 01000101 00110111 00110100 00110100 01000100 00110100 00111001 00110101 00110111 00110111 00110011 00110111 01000001 00110101 00111000 00110011 00110010 00110100 00110110 00110100 01000110 00110101 00111000 00110111 01000001 00110100 00110010 00110111 00110101 00110100 01000100 00110101 00110111 00110011 00111001 00110111 00110101 00110101 00111000 00110110 01000101 00110011 00110000 00110011 01000100'

layer1 = ''.join(chr(int(b, 2)) for b in binary.split())
layer2 = bytes.fromhex(layer1).decode()
layer3 = base64.b64decode(layer2).decode()
print(layer3)
```

---

## Flag

```
boroCTF{L!k3_aN_0n1on^}
```

---

## Key takeaways

- Recognize encoding by its "fingerprint": binary = groups of 8 bits (0/1 only); hex = even length, only `0-9A-F`; base64 = alphanumeric + `+/=`
- When stuck mid-chain, paste the intermediate result into CyberChef and click **Magic** — it auto-detects common encodings
- Beware of tools that suggest "possible coordinates" or other interpretations when you're mid-chain — these are false positives, not rabbit holes
- Standard encoding chain in CTF: **binary → hex → base64 → plaintext** — memorize this order
