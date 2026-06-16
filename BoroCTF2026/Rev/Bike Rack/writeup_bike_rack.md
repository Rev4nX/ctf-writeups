# boroCTF 2026 — Bike Rack (Rev, 200pts)

**Author:** Franklin
**Category:** Rev

## Description

> OH NO!!! You forgot the PIN for your bike lock. Analyze the lock and figure out how to break it.

## Files

- `chal` — ELF 64-bit PIE executable, stripped

---

## Overview

This writeup is intentionally written as a **case study split into separate steps**, each one a self-contained mini-writeup. The goal isn't just the flag — it's a reusable methodology for "RE challenge with a hidden flag and obfuscated strings." Each step states *what you observe*, *what question it forces you to ask*, and *what action follows*.

The flag is: `boroCTF{R@nd00M_YZ42u%ym}`

---

# Step 0 — Triage: what kind of challenge is this?

### Observation

```bash
$ file chal
chal: ELF 64-bit LSB pie executable, x86-64, stripped

$ strings chal | grep -iE "boro|CTF|flag"
# (nothing)
```

### Question it forces

`strings` finds no flag. Why? Three possibilities:
1. The flag is built at runtime (concatenated/computed, never stored as one contiguous string)
2. The flag is encrypted/encoded in the binary
3. The flag is hidden inside a larger string so `grep` for `boro` doesn't isolate it

### Action

The empty `grep` result is **information, not a dead end**. It tells you the author deliberately hid the flag. This is a reversing challenge, not a "grep the strings" challenge. Move to a decompiler (Ghidra).

### Critical refinement — grep hid the answer, not `strings`

`strings | grep` filters by an exact word. If the flag doesn't contain the literal letters `flag` or `boro` as adjacent characters, grep throws it away with everything else. Run `strings` with **no grep** (or `strings chal | less`) and the interesting data is right there:

```
AweQbLpMnorTyUioZxcvbnmCQwertyuioTqwFer{TyUiopasRd@fghjknLzXcvbnmdQwerty0u0IopasdMFghjklzxc_VbnmqwerYCvbnZMqw4e2RtyuiopasuFghjklzx%SdfyGhjklzmNbmqwerty}
1927591750185873109357128735:912357132509713257561029375701027357361:2179327561242142098:980985641877731:238
187773102385012356629012836224235219768597857
```

Three things jump out to the eye that grep can never match:
1. A string containing `{` and `}` — a flag is in there, just scrambled into junk (the letters `b-o-r-o` are not adjacent, so `grep boro` misses it)
2. A long colon-separated digit string — screams "encoded key / PIN"
3. A second digit string (the one `strncat` appends)

### Takeaway

> `strings | grep flag` is the fast first shot; `strings` with **no grep** is the mandatory second shot. grep narrows by a word you have to guess; your eye catches patterns grep doesn't know — long digit runs, strings with `{}`, base64-like blocks, odd custom alphabets. An empty `grep` is a positive signal (flag is obfuscated), but it is NOT a reason to stop looking at `strings` output.

---

# Step 1 — Read the decompilation and trace the input

### Observation

Ghidra gives this `main` (cleaned up):

```c
printf("...PIN: ");
strlen(&DAT_00104120);
memmove(&DAT_00104120, s_..._00104128, sVar1 - 7);
strncat(&DAT_00104120, "187773102385012356629012836224235219768597857", 0xb);

fgets(&DAT_00104240, 0x100, stdin);          // <-- user input lands here
strcspn(&DAT_00104240, "\r\n"); ... = 0;     // strip trailing newline
```

### Question it forces

*Where does my input go, and what reads it afterward?*

Your input goes into `DAT_00104240`. That is the buffer to follow. Everything that touches `DAT_00104240` downstream is the real algorithm.

### Action

Mark `DAT_00104240` as "USER INPUT" and trace every subsequent use of it. Mark `DAT_00104120` as "something else, built before input is even read — verify later whether it's used."

### Takeaway

> The first move in any RE is: identify the input buffer and follow it. Everything else is either preprocessing, output, or misdirection until proven otherwise.

---

# Step 2 — Separate signal from misdirection

### Observation

Before reading input, the program does:

```c
strlen(&DAT_00104120);
memmove(&DAT_00104120, s_..._00104128, sVar1 - 7);
strncat(&DAT_00104120, "1877731...", 0xb);
```

This builds a string in `DAT_00104120`. Then... `DAT_00104120` is **never referenced again** in the rest of `main`.

### Question it forces

*Is `DAT_00104120` ever read after being built?* Search the function. It is not used in either processing loop.

So what is it? Two hypotheses:
- (A) Pure red herring to waste your time
- (B) It IS the PIN you're meant to type — built dynamically so it never appears in `strings`

Hold both hypotheses. Don't commit yet.

### Action

Note the contradiction and keep reading. The algorithm operates only on `DAT_00104240` (your input). Whatever `DAT_00104120` is, it doesn't feed the algorithm directly — but it might be the *answer* you feed in.

### Takeaway

> A variable that is written but never read in the same scope is suspicious. In CTF RE it's usually one of two things: a decoy, or the expected input constructed off-screen to dodge `strings`. Both are worth resolving — don't ignore it.

---

# Step 3 — Understand the algorithm, loop by loop

### Observation — Loop 1 (the "stride" loop)

```c
local_138 = 0;
for (local_130 = 0; local_130 < strlen(&DAT_00104240); local_130 += 4) {
    local_118[local_138] = (&DAT_00104240)[local_130];
    local_138++;
}
local_118[local_138] = '\0';
```

### What it does

Walks your input taking **every 4th character** (indices 0, 4, 8, 12, ...) and packs them into `local_118`. A 111-char input becomes ~28 chars. The other 3-of-4 characters are pure padding — they exist only to space out the meaningful digits.

### Observation — Loop 2 (the "accumulator → lookup" loop)

```c
local_140 = 0;
for (local_128 = 0; local_128 < strlen(local_118); local_128++) {
    local_140 = local_140 + local_118[local_128] - 0x30;   // 0x30 == '0'
    putchar(s_AweQbLpMnor..._00104020[local_140 - 1]);
}
putchar(10);
```

### What it does

- `c - 0x30` converts an ASCII digit to its numeric value (`'7'` → 7).
- `local_140` is a **running accumulator** — each digit adds to it.
- The accumulator is used as an **index** into a big lookup string (at `0x104020`), and `lookup[local_140 - 1]` is printed.

So the output character `n` depends on the *sum of all digit values so far*. The PIN is a sequence of "jumps" that walk the accumulator to exactly the indices where the flag characters live inside the lookup string.

### Question it forces

*What is in that lookup string, and where do the flag characters sit inside it?* You can't answer this from Ghidra's truncated symbol name — you need the raw bytes.

### Takeaway

> Decompile the *control flow* first (what transforms what), then go fetch the *data* it operates on. Here: "take every 4th char, treat digits as deltas into a string." That mental model is all you need before extracting data.

---

# Step 4 — Extract exact data from the binary

### Observation

Ghidra shows `s_AweQbLpMnorTyUioZxcvbnmCQwertyui_00104020` — but truncated. You need the *full* contents. Dump the raw sections:

```bash
$ objdump -s -j .data chal
$ objdump -s -j .rodata chal
```

`.data` at `0x4020` (the lookup string):

```
AweQbLpMnorTyUioZxcvbnmCQwertyuioTqwFer{TyUiopasRd@fghjknLzXcvbnm
dQwerty0u0IopasdMFghjklzxc_VbnmqwerYCvbnZMqw4e2RtyuiopasuFghjklzx
%SdfyGhjklzmNbmqwerty}
```

Length: 152 characters. And look — it contains `{`, `}`, `@`, `_`, `%`, `4`, `2`, `0` scattered through it. **The flag is embedded inside this string**, mixed into junk filler.

`.data` at `0x4120` (the mystery `DAT_00104120` buffer, *initial* contents):

```
1927591750185873109357128735:9123571325097132575610293757010273573
61:2179327561242142098:980985641877731:238
```

`.rodata` at `0x2058` (the string `strncat` appends from):

```
187773102385012356629012836224235219768597857
```

### Action

Now you can resolve Step 2's hypothesis (B): `DAT_00104120` holds a long digit string. The flag is confirmed to be inside the `0x4020` lookup string. The PIN must be the thing that navigates to it.

### Takeaway

> Ghidra symbol names are previews, not ground truth. For exact bytes — string contents, array initializers, embedded blobs — use `objdump -s` (or `xxd` on the right offset). Always extract the real data before writing a solver.

---

# Step 5 — Reconstruct the PIN

### Observation

The PIN is `DAT_00104120` after two operations:

```c
sVar1 = strlen(&DAT_00104120);              // length of initial string = 108
memmove(&DAT_00104120, &DAT_00104120 + 8, sVar1 - 7);   // shift left by 8, copy 101 bytes
strncat(&DAT_00104120, "1877731...", 0xb);  // append first 11 chars
```

Two subtleties that are easy to get wrong:
- `s_..._00104128` is at address `0x4128`, which is `0x4120 + 8`. So the memmove source is `DAT_00104120 + 8`, i.e. the initial string starting from offset 8.
- `sVar1 - 7` where `sVar1 = 108` → copies 101 bytes. Combined with the +8 offset, this takes `initial[8 : 8+101]`.

### Action — reconstruct in Python

```python
initial = ("1927591750185873109357128735:9123571325097132575610293757010273573"
           "61:2179327561242142098:980985641877731:238")
# strlen == 108
n = len(initial) - 7                       # 101
shifted = initial[8 : 8 + n]               # memmove: source offset +8
append = "187773102385012356629012836224235219768597857"[:0xb]  # first 11 chars
pin = shifted + append
print(pin)
```

Result (111 digits, with literal `:` separators from the original buffer):

```
50185873109357128735:912357132509713257561029375701027357361:2179327561242142098:980985641877731:23818777310238
```

### Takeaway

> When reconstructing string manipulation, the two classic traps are **off-by-N offsets** (here the `+8` from the address gap `0x4128 - 0x4120`) and **length arithmetic** (`sVar1 - 7`). Recompute lengths explicitly; don't eyeball them.

---

# Step 6 — Write the solver and verify against the real binary

### Action — simulate the algorithm in Python

```python
lookup = ("AweQbLpMnorTyUioZxcvbnmCQwertyuioTqwFer{TyUiopasRd@fghjknLzXcvbnm"
          "dQwerty0u0IopasdMFghjklzxc_VbnmqwerYCvbnZMqw4e2RtyuiopasuFghjklzx"
          "%SdfyGhjklzmNbmqwerty}")

def simulate(inp):
    extracted = inp[::4]          # Loop 1: every 4th char
    acc = 0
    out = ""
    for c in extracted:           # Loop 2: accumulator -> lookup index
        acc += ord(c) - 0x30
        out += lookup[acc - 1]
    return out

pin = "50185873109357128735:912357132509713257561029375701027357361:2179327561242142098:980985641877731:23818777310238"
print(simulate(pin))
```

Output: `boroCTF{R@nd00M_YZ42u%ym}???` (trailing `?` = accumulator running past the flag; the binary stops at `}`).

### Action — verify on the live binary (do not trust the simulation alone)

```bash
$ echo "50185873109357128735:912357132509713257561029375701027357361:2179327561242142098:980985641877731:23818777310238" | ./chal
Hey, uhm, why are there so many different inputs for this bike lock???
PIN: boroCTF{R@nd00M_YZ42u%ym}
```

### Takeaway

> A Python simulation can have the same bug twice (in your reading and your reimplementation). Confirming on the real binary is the only thing that proves you understood it. Hypothesis from analysis != result; run the verification.

---

## Flag

```
boroCTF{R@nd00M_YZ42u%ym}
```

---

## Master takeaways (the reusable method)

- **Empty `strings | grep` = "flag is obfuscated"**, a clue not a wall — switch to decompilation
- **Find the input buffer first**, then trace only what touches it; everything else is preprocessing, output, or decoy until proven otherwise
- **Written-but-never-read variable** = decoy OR off-screen-constructed expected input (here: the PIN, built dynamically to evade `strings`)
- **Decompile control flow, then extract data** — understand *what transforms what* before fetching the bytes it transforms
- **`objdump -s` for exact bytes** — Ghidra symbol names are truncated previews, not ground truth
- **Off-by-N and length arithmetic are the classic reconstruction traps** — recompute lengths and offsets explicitly (`0x4128 - 0x4120 = 8`)
- **Embedded-flag-in-junk pattern**: the flag lives inside a big lookup string, and the "key" (PIN) is a sequence of accumulator deltas that index exactly its characters
- **Always verify on the real binary** — a simulation can replicate your own misreading
