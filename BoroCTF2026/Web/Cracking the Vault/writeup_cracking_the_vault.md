# boroCTF 2026 — Cracking the Vault (Web, 100pts)

**Author:** Solarity  
**Category:** Web  

## Description

> Apparently this banking system is super secure and would never store the password somewhere in plain sight...

## URL

`https://qphi2o7slkwc.boroctf.com/`

---

## Solution

### Step 1 — View the page source

The description hints that the password is stored "in plain sight." Open the raw HTML source with **Ctrl+U**.

### Step 2 — Find the password in JavaScript

In the `<script>` block, the password is hardcoded as a JavaScript constant:

```javascript
const correctPassword = "passworduwu";
```

Client-side password validation is fundamentally broken — the browser downloads all the JavaScript, which means the user can read it. There is no way to hide a secret inside code that runs on the visitor's machine.

### Step 3 — Two ways to get the flag

Both the password and the flag are hardcoded in the JavaScript — everything runs locally in the browser, no server is involved.

**Method A — Read the flag directly from source**  
The flag is visible as a string literal in the `if` branch, right there in the source. No need to interact with the page at all.

**Method B — Submit the password**  
Enter `passworduwu` in the input field and click Unlock. The page renders:

```
✓ Correct! Flag: boroCTF{th3_p@th_l3ss_tr@vers3d}
```

This is what most players do instinctively — find the password, submit it, get the flag. Both approaches work because both secrets live in the client-side JavaScript.

---

## Flag

```
boroCTF{th3_p@th_l3ss_tr@vers3d}
```

---

## Key takeaways

- **Never validate passwords client-side.** Any secret in JavaScript is readable by anyone who opens the source — the browser has to download the code to run it
- This is a different hiding technique from the previous challenge (HTML comment) but the same discovery method: Ctrl+U → read the source
- When you see a login form in a web challenge, always check the source before trying anything complex — the password is often hardcoded right there
- Both the password and the flag are hardcoded in client-side JavaScript — no server request is needed at any point. There are two valid methods: read the flag directly from source, or find the password in source and submit it
