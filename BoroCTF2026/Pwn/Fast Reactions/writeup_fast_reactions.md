# boroCTF 2026 — Fast Reactions (Pwn, 100pts)

**Author:** Franklin  
**Category:** Pwn  

## Description

> Need higher WPM? Try monkeytype.

## Server

`nc tnkemaq46125.boroctf.com 56354`

---

## Solution

### Step 1 — Understand the challenge

Connecting manually reveals the mechanic:

```
Please enter 0x69 characters!
```

The server asks for a specific number of characters in hex. Sending too few returns "Too short!", too many returns "Too long!". Sending exactly the right number returns the flag.

The number is random each connection, and the time window is too short for a human to count and type the correct number of characters. This is a classic "impossible for a human, trivial for a script" challenge.

### Step 2 — Write a solver

Using `pwntools` — the standard Python library for PWN challenges:

```python
from pwn import *

conn = remote('tnkemaq46125.boroctf.com', 56354)

for _ in range(100):
    line = conn.recvline().decode().strip()
    print(line)
    
    if 'boroCTF' in line:
        print("FLAG:", line)
        break
    
    if 'Please enter' in line:
        count = int(line.split('0x')[1].split(' ')[0], 16)
        conn.sendline(b'a' * count)

conn.close()
```

The script:
1. Reads a line from the server
2. If it contains the flag — prints it and stops
3. If it says "Please enter 0xNN characters" — parses the hex number and sends exactly that many `a` characters
4. Repeats up to 100 times

### Step 3 — Run it

```bash
python3 solver.py
```

Output:

```
[+] Opening connection to tnkemaq46125.boroctf.com on port 56354: Done
Please enter 0x60 characters!
Nice job! Flag: boroCTF{Hum@n1y_im7o5s!ble}
FLAG: Nice job! Flag: boroCTF{Hum@n1y_im7o5s!ble}
[*] Closed connection to tnkemaq46125.boroctf.com port 56354
```

---

## Flag

```
boroCTF{Hum@n1y_im7o5s!ble}
```

---

## Key takeaways

- **"Impossible for a human, trivial for a script"** is a classic CTF pattern — the challenge is recognizing that automation is the solution, not typing faster
- `pwntools` is the standard Python library for PWN and network-based challenges — `remote()` connects to a server, `recvline()` reads a line, `sendline()` sends data
- Hex parsing: `int('0x60', 16)` = 96 — always convert hex to decimal before using as a count
- Save scripts to a file with `nano solver.py` or a heredoc (`cat > solver.py << 'EOF'`) — running complex Python through `-c` with nested quotes causes syntax errors
