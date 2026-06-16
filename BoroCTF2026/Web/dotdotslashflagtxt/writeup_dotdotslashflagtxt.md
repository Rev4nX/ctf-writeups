# boroCTF 2026 — dotdotslashflagtxt (Web, 100pts)

**Author:** Solarity  
**Category:** Web  

## Description

> A company left their internal document viewer exposed. It only shows approved files... or does it?

## URL

`https://0gil6sh8nlk1.boroctf.com/`

---

## Solution

### Step 1 — Identify the attack surface

The site is a document viewer listing three publicly available files: `readme.txt`, `notes.txt`, `about.txt`. Clicking any of them opens it via a `file` parameter in the URL:

```
https://0gil6sh8nlk1.boroctf.com/view?file=about.txt
```

One of the documents (about.txt) hints directly at the target:

```
We hold many secrets, like a flag.txt in a folder outside of public view.
```

### Step 2 — Path traversal

The challenge name says it all: `dotdotslashflagtxt` = `../flag.txt`.

The server takes the `file` parameter and appends it to a base directory path, something like:

```python
path = "/var/www/documents/" + request.args["file"]
open(path)
```

If the application doesn't validate that the resulting path stays inside the allowed directory, `../` causes the OS to step up one level in the filesystem — completely standard filesystem behavior, not a web-specific trick.

Substituting `../flag.txt` as the file parameter:

```
https://0gil6sh8nlk1.boroctf.com/view?file=../flag.txt
```

The server resolves `/var/www/documents/../flag.txt` → `/var/www/flag.txt` and serves the file.

---

## Vulnerability: Path Traversal (Directory Traversal)

Path traversal is a vulnerability where user-supplied input is passed directly to filesystem operations without sanitization. By injecting `../` sequences, an attacker can escape the intended directory and read arbitrary files on the server.

The proper fix is to resolve the full path first and then verify it still starts with the allowed base directory before opening the file.

`..` is a filesystem convention, not a web one — it works on Linux, Windows, and any other OS with a hierarchical filesystem. On Windows, both `../` and `..\` are valid; on Linux only `/` works as a separator.

---

## Flag

```
boroCTF{p@th_Tr@v3rs@L_r0Ck5!}
```

---

## Key takeaways

- Whenever you see a `?file=` or `?path=` parameter in a URL, try path traversal — it's one of the first things to check on web challenges
- The number of `../` needed depends on how deep the base directory is; start with one and add more if it doesn't work
- `..` is a filesystem concept, not web-specific — the vulnerability is in the backend code blindly passing user input to the OS
- The challenge name was the entire hint: `dotdotslashflagtxt` = `../flag.txt`
