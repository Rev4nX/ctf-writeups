# boroCTF 2026 — Physical Access >> (OSINT, 100pts)

**Author:** Solarity  
**Category:** OSINT  

## Description

> Help!! I forgot my password and got locked out of my Windows PC!  
> I need to get back in, what can I do?!  
> What is one of the two files I can exploit in order to get back into my PC?  
> Flag format: `boroCTF{explorer.exe}`

---

## Solution

### Background — Windows Accessibility Executables

Windows has a set of accessibility tools that can be launched directly from the login screen, **before any user is authenticated**. This is by design — blind or motor-impaired users need to be able to activate screen readers or keyboard assistance before logging in.

The two most commonly exploited executables are:

**`sethc.exe`** — Sticky Keys  
Triggered by pressing the Shift key 5 times in rapid succession. Windows shows a dialog asking if you want to enable Sticky Keys (a feature for users who can't hold multiple keys simultaneously). This executable runs as **SYSTEM** — the highest privilege level in Windows, above even Administrator.

**`utilman.exe`** — Utility Manager  
Triggered by clicking the accessibility icon in the bottom-right corner of the login screen (or pressing Win+U). Opens a panel with accessibility options like Narrator, Magnifier, On-Screen Keyboard. Also runs as **SYSTEM**.

### The Attack

The classic technique (known since at least Windows XP, still partially relevant today):

1. Boot from a live USB or recovery environment (e.g. Windows Recovery, Linux live USB)
2. Mount the Windows partition
3. Navigate to `C:\Windows\System32\`
4. Replace `sethc.exe` or `utilman.exe` with a copy of `cmd.exe`:
   ```
   copy cmd.exe sethc.exe
   ```
   (or rename/swap the files)
5. Reboot normally into Windows
6. At the login screen, trigger the accessibility shortcut (5x Shift for sethc, Win+U for utilman)
7. A Command Prompt opens **as SYSTEM** — no password required
8. Use `net user Administrator newpassword` to reset any account password
9. Log in normally

### Why This Works

The accessibility executables are designed to run before authentication. Windows does not verify whether they have been tampered with at runtime. Since they run as SYSTEM, anything you launch through them (like CMD) inherits SYSTEM privileges — giving you full control over the machine.

### Mitigations

Modern Windows (10/11) with Secure Boot enabled and Windows Defender Credential Guard makes this harder but not impossible. BitLocker encryption also helps — if the drive is encrypted, mounting it from a live USB to swap the files is blocked without the recovery key.

---

## Flag

```
boroCTF{sethc.exe}
```

---

## Key takeaways

- `sethc.exe` (Sticky Keys) and `utilman.exe` (Utility Manager) run as SYSTEM from the Windows login screen before authentication
- Replacing either with `cmd.exe` gives a SYSTEM shell without knowing any password
- Physical access to a machine without full-disk encryption (BitLocker) = effectively no security
- This is why "physical access = game over" is a core principle in security — software protections mean little if an attacker can boot from external media
