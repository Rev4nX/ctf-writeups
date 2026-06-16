# boroCTF 2026 — George Orwell (REV, 100pts)

**Author:** Franklin  
**Category:** Reverse Engineering  
**Points:** 100  

## Description

> Big Brother says: We're always watching. Your words, no matter how silent, will be heard.  
> Note - This challenge simulates real malware but contains NO malicious payloads.

## Files

- `big_brother`

---

## Solution

### Step 1 — Identify the file type

```bash
file big_brother
# big_brother: PE32 executable (GUI) Intel 80386, for MS Windows, 4 sections
```

A 32-bit Windows GUI executable. GUI means no console window by default.

### Step 2 — Extract strings

The description hints at keylogging ("your words will be heard"). Combined with the file being a Windows executable, AutoHotkey is a likely candidate — it compiles scripts into EXEs but stores the original source code as plaintext inside the binary.

```bash
strings big_brother | grep -i boro
```

Output:
```
:*:iloveboroctf::
```

This is an AutoHotkey hotstring — a macro that fires when you type `iloveboroctf` in any application.

### Step 3 — Extract the full script

```bash
strings big_brother | grep -A2 -B2 "iloveboroctf"
```

The full relevant section:

```
:*:iloveboroctf::
secret := Chr(98) . Chr(111) . Chr(114) . Chr(111) . Chr(67) . Chr(84) . Chr(70) . Chr(123)
secret := secret . Chr(65) . Chr(72) . Chr(75) . Chr(95) . Chr(49) . Chr(115) . Chr(95)
secret := secret . Chr(108) . Chr(73) . Chr(115) . Chr(43) . Chr(101) . Chr(110) . Chr(105)
secret := secret . Chr(52) . Chr(103) . Chr(125)
MsgBox, 64, System Notification, Access Granted!`n`nFlag: %secret%
```

### Step 4 — Decode the flag

In AutoHotkey, `Chr(n)` returns the character with ASCII code `n`. The `.` operator concatenates strings. `secret := secret . Chr(...)` is AutoHotkey's equivalent of Python's `secret += chr(...)`.

We extract all numbers from `Chr()` calls and decode them in Python:

```python
import re

ahk = """
secret := Chr(98) . Chr(111) . Chr(114) . Chr(111) . Chr(67) . Chr(84) . Chr(70) . Chr(123)
secret := secret . Chr(65) . Chr(72) . Chr(75) . Chr(95) . Chr(49) . Chr(115) . Chr(95)
secret := secret . Chr(108) . Chr(73) . Chr(115) . Chr(43) . Chr(101) . Chr(110) . Chr(105)
secret := secret . Chr(52) . Chr(103) . Chr(125)
"""

codes = re.findall(r'Chr\((\d+)\)', ahk)
print(''.join(chr(int(c)) for c in codes))
```

---

## Flag

```
boroCTF{AHK_1s_lIs+eni4g}
```

---

## Key takeaways

- AutoHotkey compiles scripts into EXEs by bundling the interpreter + original source as plaintext — `strings` is enough to read the full script
- The "keylogger" pattern: `:*:trigger::` hotstring intercepts keypresses system-wide, in any application
- `Chr(n)` encoding is trivial to reverse — just map ASCII codes to characters
- `strings | grep` is often the fastest first step on any unknown Windows binary
