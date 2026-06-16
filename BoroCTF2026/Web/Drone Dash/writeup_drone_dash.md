# boroCTF 2026 — Drone Dash (Web, 100pts)

**Author:** ForeverFlames  
**Category:** Web  

## Description

> Welcome to the neon grid, pilot. Your objective is simple: Land the drone on the pad in under 1.5 seconds.

## URL

`https://697vj046dbi3.boroctf.com`

---

## Solution

### What the challenge is supposed to be

The page presents a drone flight simulator. You send a JSON flight profile to `/api/flight-profile`:

```json
{
  "physics": {
    "Kp": 0.1,
    "Kd": 0.5,
    "Ki": 0.01
  }
}
```

The server simulates a PID controller flight and responds with either `WIN` (flight time < 1.5s) or `FAIL` (estimated default: 3.5s). The intended exploit is **prototype pollution** — injecting `__proto__` into the JSON to manipulate internal server objects and trick the flight time check.

The intended payload would look something like:

```json
{
  "__proto__": {
    "flightTime": 0.5
  },
  "physics": {
    "Kp": 0.1,
    "Kd": 0.5,
    "Ki": 0.01
  }
}
```

If the server merges user input into an internal object without sanitization (e.g. via `Object.assign`), injecting `__proto__` poisons `Object.prototype` — every object in the application inherits the injected property, including the one that checks whether the flight time is under 1.5 seconds.

### What actually happened

The challenge was misconfigured: the default JSON values already return `WIN` from the server without any modification. Clicking "INITIATE FLIGHT" with the pre-filled JSON immediately returns the flag.

---

## Vulnerability: Prototype Pollution

Prototype pollution is a JavaScript-specific vulnerability where an attacker can inject properties into `Object.prototype` by supplying `__proto__` (or `constructor.prototype`) in user-controlled data that gets merged into an object without sanitization.

Since all JavaScript objects inherit from `Object.prototype`, poisoning it affects every object in the runtime — including internal application state the attacker was never meant to touch.

The fix is to sanitize user input before merging: reject keys named `__proto__`, `constructor`, or `prototype`, or use `Object.create(null)` for objects that should not inherit from the prototype chain.

---

## Flag

```
boroCTF{pr0totyp3_p0llut10n_dr0ne_d4sh}
```

---

## Key takeaways

- **Prototype pollution** targets JavaScript's prototype inheritance — injecting `__proto__` into merged user input can poison `Object.prototype` and affect all objects in the application
- When you see a JSON input field in a web challenge, try adding `__proto__` with properties that might affect server-side logic
- This challenge was misconfigured — the default values already returned WIN. The flag name (`pr0totyp3_p0llut10n`) confirms what the intended exploit was supposed to be
