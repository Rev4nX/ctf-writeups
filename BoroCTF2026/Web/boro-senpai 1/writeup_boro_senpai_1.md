# boroCTF 2026 — boro-senpai 1 (Web, 100pts)

**Author:** Solarity  
**Category:** Web  

## Description

> Muhahaha! The Organization thinks they can silence me, but I, Hououin Kyouma, have uncovered a lead. My assistant — the self-proclaimed neuroscience prodigy — harbors a secret so embarrassing it could shake the very fabric of her dignity. An old @channel handle. Find it, and her profile is yours. El. Psy. Kongroo.

## URL

`https://w03xj6cjsucj.boroctf.com`

---

## Solution

### Step 1 — Understand the lore

The challenge is set in the Steins;Gate universe. "The assistant — self-proclaimed neuroscience prodigy" refers to **Maho Hiyajo**, a character from Steins;Gate 0. The goal is to find her @channel (a 4chan-style imageboard in the game's world) username and visit her profile.

### Step 2 — Find the username in the forum

The site contains a fictional imageboard. Reading the threads on `/sg/ - Steins;Gate`, one username stands out as unusually knowledgeable about temporal mechanics and clearly matches Maho's character:

```
KuriGohanandKamehameha
```

She posts in multiple threads under this handle, including a detailed discussion of Novikov self-consistency and conservation of energy — very on-brand for a neuroscience researcher.

### Step 3 — IDOR: access her profile directly

Profiles are accessible at predictable URLs: `/profile/<username>`. The logged-in account (`hououin_kyouma`) is at:

```
/profile/hououin_kyouma
```

This pattern means any user's profile is reachable by substituting their username. Navigate to:

```
https://w03xj6cjsucj.boroctf.com/profile/KuriGohanandKamehameha
```

The server returns her full profile — including the flag in the FLAG field.

---

## Vulnerability: IDOR (Insecure Direct Object Reference)

IDOR is a web vulnerability where an application exposes internal objects (users, files, records) through predictable identifiers in the URL, without verifying that the requester is authorized to access that specific object.

Here, the "object" is a user profile and the "reference" is the username in the URL. The server never checks whether the logged-in user has permission to view someone else's profile — it just returns whatever matches the URL. Changing the username is enough to access any account.



---

## Flag

```
boroCTF{3l_psY_c0ngR00!}
```

---

## Key takeaways

- When you see a profile URL like `/profile/your_username`, always try substituting other usernames — IDOR is extremely common in CTF web challenges
- The username came directly from reading the forum content — no technical tools needed, just careful reading
- The site also has profiles for `super_hacka_daru` (Itaru Hashida) and `mayushii_ttm` (Mayuri Shiina) with no flags — purely for lore, worth checking out if you're a Steins;Gate fan
