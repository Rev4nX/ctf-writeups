# boroCTF 2026 — kitty kitty meow meow (Forensics, 100pts)

**Author:** Solarity  
**Category:** Forensics  

## Description

> aww... so cute!

## Files

- `meow.jpg`

---

## Solution

### Step 1 — Check strings

The file is a JPEG image of a cat. First step for any unknown file: extract all readable strings.

```bash
strings meow.jpg | grep -i "boro"
```

Output:
```
boroCTF{f0r3nsic_@nalysis#}
```

Flag was embedded as plaintext inside the JPEG binary data.

---

## Flag

```
boroCTF{f0r3nsic_@nalysis#}
```

---

## Key takeaways

- `strings` is always the first step on any file — it costs nothing and sometimes solves the challenge immediately
- JPEG files can contain arbitrary text data appended or embedded in comments/metadata
- On Linux/WSL: `strings file | grep -i "boro"`. On Windows PowerShell: `strings file | Select-String "boro"`
