# boroCTF 2026 — Flight (Crypto, 100pts)

**Author:** Franklin  
**Category:** Crypto  

## Description

> dark, darker, yet darker.
> `♌︎□︎❒︎□︎👍︎❄︎☞︎❀︎⬥︎✋︎■︎♑︎📂︎■︎🕯︎♉︎✏︎⧫︎❝︎`

---

## Solution

### Step 1 — Recognize the hint

"Dark, darker, yet darker" is a reference to Deltarune/Undertale (video game). In Undertale, the character W.D. Gaster communicates exclusively in **Wingdings** — a font that replaces letters with symbols. The description is a direct reference to this character and his font.

### Step 2 — Decode Wingdings

Paste the symbols into a Wingdings translator:

https://lingojam.com/WingdingsTranslator

Select "Wingdings to English" direction and paste the ciphertext. Output:

```
boroCTF{wIng1n'_!t}
```

---

## Flag

```
boroCTF{wIng1n'_!t}
```

---

## Key takeaways

- Wingdings is a **font**, not a cipher — standard cipher identifiers (CyberChef Magic, dcode.fr) will not detect it automatically
- The giveaway is a mix of emoji-like symbols that don't belong to any standard cipher alphabet — when you see this pattern in a CTF, think fonts (Wingdings, Webdings, Symbol)
- Cultural context matters: "dark, darker, yet darker" + symbol text = Undertale/Deltarune reference = Wingdings. Knowing the source material is the key
- Use https://lingojam.com/WingdingsTranslator — simpler and more reliable than dcode.fr for this specific font
- After this challenge, Wingdings is a pattern you'll recognize immediately in future CTFs
