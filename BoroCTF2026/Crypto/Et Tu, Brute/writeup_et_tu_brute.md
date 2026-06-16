# boroCTF 2026 — Et Tu, Brute (Crypto, 100pts)

**Author:** ForeverFlames  
**Category:** Crypto  

## Description

> Stabbed by his own men. Each stab wound marked how betrayed he was. Can you reverse the damage?  
> `erurFWI{@iu13qgq0pru3}`

---

## Solution

### Step 1 — Recognize the cipher

"Et Tu, Brute" is Julius Caesar's last words before being stabbed by Brutus. This is a direct reference to the **Caesar cipher** — a substitution cipher named after Julius Caesar who historically used a shift of 3.

"Each stab wound marked how betrayed he was" — historically, Caesar was stabbed **23 times**. This is the shift value.

### Step 2 — Decode

ROT23 (shift of 23 forward) = ROT3 backward (since 26 - 23 = 3).

Using CacheSleuth Cipher Identifier (https://www.cachesleuth.com/tools/cipheridentifier/) — paste the ciphertext, click Identify, and it ranks the most likely ciphers by plaintext-likeness. ROT3 (23) appears with score 26 and the correct flag.

Or manually in CyberChef: ROT13 → set amount to 23 → apply to letters only.

Note: ROT47 (all ASCII) will NOT work here — it rotates `@`, `{`, `}` as well, producing garbage. Use letters-only rotation.

### Step 3 — Understand the flag

`boroCTF{@fr13ndn0mor3}` = leet speak for "a friend no more" — Brutus, who betrayed Caesar. `@` = a, `3` = e, `1` = i, `0` = o.

---

## Flag

```
boroCTF{@fr13ndn0mor3}
```

---

## Key takeaways

- "Et Tu, Brute" + "stab wounds" = Caesar cipher with shift = number of stab wounds (23)
- Caesar cipher rotates only letters A-Z — digits and special characters stay unchanged
- ROT23 forward = ROT3 backward (26 - 23 = 3)
- **Never use ROT47** for classic Caesar — it rotates all ASCII including `@{}` and breaks the flag format
- **CacheSleuth Cipher Identifier** (https://www.cachesleuth.com/tools/cipheridentifier/) tries 250+ ciphers and ranks by English-likeness — bookmark it for unknown ciphertexts
