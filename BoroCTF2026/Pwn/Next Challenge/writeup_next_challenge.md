# boroCTF 2026 — Next Challenge (Pwn, 100pts)

**Author:** Franklin  
**Category:** Pwn  

## Description

> Psst...I've been hearing some rumors about this special command called nc. I don't know what it is so I have to assume it means Next Challenge ... right?? Maybe that MAN has more answers.

## Server

`nc thww9zyp6ygt.boroctf.com 19350`

---

## Solution

### Step 1 — Connect

```bash
nc thww9zyp6ygt.boroctf.com 19350
```

Output:

```
======================
WELCOME TO VULNBOT!!!
======================
You will need to figure out how to exploit my expert design.
help - list commands
```

### Step 2 — Read the menu

```
> help
1. cheese
2. flag
```

### Step 3 — Ask for the flag

```
> flag
Are you SURE you don't want to see what the Cheese option does? (y/n)
y
FINE. I guess if you insist.
boroCTF{0nLinE_C@ts*}
```

That's it.

---

## The cheese trap

Out of curiosity, selecting `cheese` instead:

```
> cheese
YOU HAVE BEEN DUPED BY VULNBOT!
Your curiosity was your downfall.
```

The author planted a decoy option. The challenge name "Next Challenge" and the hint "MAN has more answers" (`man nc` = the manual for netcat) were nudging players to learn what `nc` is, connect, and simply ask for the flag — not get distracted by cheese.

---

## Flag

```
boroCTF{0nLinE_C@ts*}
```

---

## Key takeaways

- Always run `help` when connecting to an unknown service — the server often tells you exactly what commands are available
- Not every PWN challenge requires an exploit — sometimes the vulnerability is that the server just... gives you the flag if you ask
- The hint "MAN has more answers" = `man nc` = the Unix manual for netcat, suggesting players who didn't know what `nc` was should read the manual first
