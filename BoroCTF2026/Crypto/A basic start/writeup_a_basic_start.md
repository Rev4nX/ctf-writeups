# boroCTF 2026 — A basic start (Crypto, 100pts)

**Author:** Franklin  
**Category:** Crypto  

## Description

> We, the Boro Cyber Division have been spying on the chats of a group of local hackers. We used to be able to decrypt their chats from base64 but they seemed to have changed their encoding. Can you find out what they're talking about now?

## Files

- `chal.txt`

---

## Solution

### Step 1 — Analyze the file

The file contains two sections:

```
Before new encoding:
VXNlcjE6IEhleSwgSSB0aGlu...==
After New encoding:
j2_1+iZB_6AveF[p/Uxg,WT[#F]4pE&m...
```

The "Before" section decodes trivially with base64 — it's a chat log between three users discussing switching to a new encoding.

### Step 2 — Identify the new encoding

The "After" section contains characters like `[`, `]`, `{`, `}`, `(`, `)`, `<`, `>`, `|`, `~` — these are not present in base64 or base85. This character set is characteristic of **base91**, a less common encoding that uses 91 printable ASCII characters.

Note: CyberChef does not have base91 — use Python instead.

### Step 3 — Decode

```python
import base91  # pip install base91

data = 'j2_1+iZB_6AveF[p/Uxg,WT[#F]4pE&m:%gZ6=0{8!Z%F.0Dj2_1rjZB!8O;R@RnqM_1:WGk$yV%J_;mz2gZY^rN$F90axFl]UgZk>;N%y60;mYiSP8=SH)S<Ry*yCrbVu_15Wy{L%;EU,fr&A2N|ir}XxI(pBZ%w<d9P'
print(base91.decode(data))
```

Or with a manual implementation — see solver script.

Output:
```
User1: Okay we're on the new encoding.
User2: You wonder if anyones ever reading your messages?
User1: Nope. boroCTF{B@5ics_0f_B@si6s}
```

---

## Flag

```
boroCTF{B@5ics_0f_B@si6s}
```

---

## Key takeaways

- When CyberChef fails, analyze the character set manually — certain characters like `[]{}|~` uniquely identify base91
- Base91 uses 91 printable ASCII characters, making encoded output shorter than base64 but with a less standard alphabet
- CyberChef doesn't have base91 — use https://www.better-converter.com/Encoders-Decoders/Base91-Decode online, or `pip install base91` in Python
- After this challenge, you'll recognize `[]{}|~` in encoded data as a base91 fingerprint
