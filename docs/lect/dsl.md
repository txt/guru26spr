<p align="center">
  <a href="https://github.com/txt/guru26spr/blob/main/README.md"><img 
     src="https://img.shields.io/badge/Home-%23ff5733?style=flat-square&logo=home&logoColor=white" /></a>
  <a href="https://github.com/txt/guru26spr/blob/main/docs/lect/syllabus.md"><img 
      src="https://img.shields.io/badge/Syllabus-%230055ff?style=flat-square&logo=openai&logoColor=white" /></a>
  <a href="https://docs.google.com/spreadsheets/d/1xZfIwkmu6hTJjXico1zIzklt1Tl9-L9j9uHrix9KToU/edit?usp=sharing"><img
      src="https://img.shields.io/badge/Teams-%23ffd700?style=flat-square&logo=users&logoColor=white" /></a>
  <a href="https://moodle-courses2527.wolfware.ncsu.edu/course/view.php?id=8119"><img 
      src="https://img.shields.io/badge/Moodle-%23dc143c?style=flat-square&logo=moodle&logoColor=white" /></a>
  <a href="https://discord.gg/vCCXMfzQ"><img 
      src="https://img.shields.io/badge/Chat-%23008080?style=flat-square&logo=discord&logoColor=white" /></a>
  <a href="https://github.com/txt/guru26spr/blob/main/LICENSE.md"><img 
      src="https://img.shields.io/badge/©%20timm%202026-%234b4b4b?style=flat-square&logoColor=white" /></a></p>
<h1 align="center">:cyclone: CSC491/591: How to be a SE Guru <br>NC State, Spring '26</h1>
<img src="https://raw.githubusercontent.com/txt/guru26spr/refs/heads/main/etc/img/banenr.png"> 



# Domain-Specific Languages: From Compartmental Models to Finite State Machines

> *"When you hit a right choice… all of a sudden things just feel right, and work speeds up enormously."*  
> — Douglas Hofstadter, *Gödel, Escher, Bach*

---

## 1. The Elbow Test

Martin Fowler asks: does your code pass the **elbow test**?  
Tim Menzies phrases it sharper: do your domain users **elbow you out of the way** in their haste to fix what is obviously wrong with your code?

If not, you are not speaking their language. You have locked out the entire community that could audit, verify, and evolve your system — the people who actually know what it should do.

That failure has a name: **accidental complexity**. The domain logic is buried under infrastructure. The *what* is entangled with the *how*.

The cure is a **Domain-Specific Language (DSL)** — a very high-level notation tailored so tightly to a problem area that an expert can learn and use it in less than a day. SQL, AWK, and regular expressions are canonical examples. But you can build your own, and that is what this lecture is about.

---

## 2. Two Flavors of DSL

| Style | Mechanism | Example |
|---|---|---|
| **External** | Parse a string; interpret it | SQL, regex, dot files |
| **Internal** | Exploit host-language features to look domain-like | Python subclasses, Lua tables |

Internal DSLs are cheaper to build. The key insight from James Martin's *Design of Real-Time Computer Systems*:

> The statistician must talk to his terminal in the language of statistics. The civil engineer must use the language of civil engineering.

The analyst's job shifts: instead of writing the application, the analyst **writes tools that let the user community write and maintain their own knowledge**.

---

## 3. The Compartmental Model: A Worked DSL in Python

### 3.1 Stock-and-Flow Thinking

Economics, ecology, software project management — all reason about *stocks* (quantities that accumulate) and *flows* (rates that change them). The canonical software example is Brooks's Law:

```
new staff → (after training delay) → productive staff → output
           ↑                                              ↓
           └────────────── management overhead ───────────┘
```

Madachy's textbook alone contains dozens of such models of software phenomena: defect injection, rework cycles, staffing dynamics. Each is a theory of how the pieces interact.

### 3.2 The DSL Pattern


```
 q   +-----+  r  +-----+
---->|  C  |---->|  D  |--> s
 ^   +-----+     +-+---+
 |                 |
 +-----------------+ 

C = stock of clean diapers
D = stock of dirty diapers
q = inflow of clean diapers
r = flow of clean diapers to dirty diapers
s = out-flow of dirty diapers
```

Flaxman and Menzies encode this theory as an *internal* Python DSL using the subclassing trick:


```python
S, A, F = Stock, Aux, Flow   # the vocabulary

class Diapers(Model):
    def have(i):
        return o(C=S(100), D=S(0), q=F(0), r=F(8), s=F(0))

    def step(i, dt, t, u, v):
        def saturday(x): return int(x) % 7 == 6
        v.C += dt * (u.q - u.r)
        v.D += dt * (u.r - u.s)
        v.q  = 70 if saturday(t) else 0
        v.s  = u.D if saturday(t) else 0
```

Notice the **separation of concerns**:
- `Model.run()` is the **engine** — it knows about time, state vectors, restraint. Users never touch it.
- `Diapers.have()` and `Diapers.step()` are the **rules** — pure domain knowledge, zero infrastructure.

A domain expert reads `v.C += dt*(u.q - u.r)` and recognises it immediately as "clean diapers accumulate from washing and deplete from use." The engine is invisible. That is the elbow test passing.

### 3.3 Debugging Philosophy

Because the model *is* the theory, debugging is theory-testing:

1. Write ten **micro-expectations** — small, falsifiable predictions about two or three variables.
2. Run and check each. Fix the theory, not the infrastructure.
3. Trust that the whole reflects the parts once the parts are right.

This is the scientific method encoded as a development practice.

---

## 4. The Finite State Machine: A DSL in Lua

### 4.1 The Same Architecture, Different Domain

`fsm3.lua` is nine lines. That is not a limitation — that is the point.

```lua
local M = {}

local function run(rules, s, p)
  if rules[s] and rules[s].action then rules[s].action(p) end
  local e = table.remove(p.queue, 1)
  if not e then return p end
  return run(rules, (rules[s].transitions[e] or s), p) end

function M.start(rules, s, p) return run(rules, s, p) end

return M
```

`run` is the **engine**: it drives time (event by event), manages the current state, and delegates all domain behaviour to the `rules` table. It is structurally identical to `Model.run()` — a loop over time, reading current state, applying the user's step function, advancing.

The **rules table** in `machine3.lua` is the DSL:

```lua
idle = {
  action      = say("is idling. HP: {hp}"),
  transitions = mix{ walk="moving", attack="attacking" }
}
```

A game designer reads this. They do not read `table.remove` or `return run(...)`. The elbow test passes.

### 4.2 The Payload as Mutable State

The FSM gains a crucial power from the `p` (payload) argument: **the machine can rewrite its own future**. In `staggered`, lethal damage injects `"die"` at the front of the event queue:

```lua
function(p) if p.hp <= 0 then inject(p, "die") end end
```

This is the FSM analogue of the compartmental model's `if t == 27: v.s = 0` — a special-case intervention written in domain language, not engine language.

---

## 5. The Generalised Pattern

Both DSLs share the same deep structure:

```
┌─────────────────────────────────────────────────────┐
│                      ENGINE                         │
│  "How time passes, how state updates, how output   │
│   is produced"                                      │
│                                                     │
│  Model.run()          fsm3.run()                    │
└──────────────────────────┬──────────────────────────┘
                           │ calls
┌──────────────────────────▼──────────────────────────┐
│                      RULES                          │
│  "What the domain knows: stocks, flows, actions,   │
│   transitions, guards"                              │
│                                                     │
│  Diapers.have()/step()   rules = { idle={...}, …}  │
└─────────────────────────────────────────────────────┘
                           │ operates on
┌──────────────────────────▼──────────────────────────┐
│                     PAYLOAD / STATE                 │
│  "The mutable world: current values, event queues, │
│   damage queues, HP, population stocks"             │
│                                                     │
│  u, v (state vectors)    p (hero table)            │
└─────────────────────────────────────────────────────┘
```

### Cognitive Framing

This architecture is not accidental. It maps to how experts think:

| Layer | Cognitive role | Who owns it |
|---|---|---|
| Engine | Execution model (universal) | Language designer |
| Rules | Domain theory (situated) | Domain expert |
| Payload | Instance data (particular) | End user |

The DSL is the **boundary** between the engine layer and the rules layer. A good DSL makes the rules layer so readable that the domain expert *owns* it — they can audit it, argue with it, fix it.

---

## 6. Idiom Extraction: The Craft of DSL Design

A DSL does not spring fully formed from the designer's head. It is **extracted from repeated idioms** in the raw code. This is the process shown in `todo.md` (Q0–Q5).

### Step 1 — Identify the Pain

`machine2.lua` contains at least four clumsy patterns:

1. **String concatenation spam** — `"[" .. p.name .. "] is idling. HP: " .. p.hp` copy-pasted into every action with tiny variations.
2. and three others.

Each clumsy pattern is a **leaking abstraction**: the engine's implementation details are bleeding into the rules layer.

### Step 2 — Name the Idiom, Write the Helper

| Idiom | Helper | Before | After |
|---|---|---|---|
| Format message with payload fields | `say(msg)` | `function(p) print("[" .. p.name .. "] is idling. HP: " .. p.hp) end` | `say("is idling. HP: {hp}")` |
| ... |---|---|---|

### Step 3 — The Resulting Language

After extraction, the rules in `machine3.lua` read almost like a design document:

```lua
staggered = {
  action = combine(
    function(p) p.hp = p.hp - pop_damage(p) end,
    say("took damage! HP: {hp}"),
    function(p) if p.hp <= 0 then inject(p, "die") end end
  ),
  transitions = mix{ recover="idle" }
}
```

A designer who has never seen Lua can read this. That is the goal.

---

## 7. Beyond Q0: The DSL as a Living System

The homework questions Q1–Q5 each add a layer to the DSL:

| Question | Feature | SE Principle |
|---|---|---|
| Q1 — Trace | `p.trace` records every `[event] from -> to` | Observability without breaking the engine |
| Q2 — Lint | Static analysis before `start` catches ghost states, dead ends, unreachable states | Fail fast; shift verification left |
| Q3 — Guards | Transition values can be functions: `return p.stamina > 10 and "attacking" or "idle"` | Conditional logic belongs in the rules, not the engine |
| Q4 — Wildcard | `t[e] or t["*"] or s` — one-line fallback | Graceful degradation; explicit over silent failure |
| Q5 — DOT export | `to_dot(rules)` generates a Graphviz diagram | The rules *are* the documentation |

Q5 is particularly striking. Because the rules table *is* the model, not a description of the model, you can **read it as data** and generate other artifacts from it — diagrams, tests, coverage reports. This is the power of treating domain knowledge as first-class structure.

---

## 8. The Bigger Lesson

DSLs are not just a coding convenience. They are a **theory of collaboration** between the people who understand computation and the people who understand the domain.

When Menzies and Geletko used a compartmental model of world population dynamics, they did not write new simulation code. They parameterised the existing model and applied optimisation. The domain knowledge was already explicit, already auditable, already separable from the engine. That is why they could find that capping family size and industrial output ratio avoided collapse — and communicate that finding to non-programmers.

The same principle applies to your RPG FSM, your build pipeline, your CI/CD state machine, your refactoring tool. Every time you find yourself writing `table.remove` inside business logic, or copy-pasting transition tables, you are paying a tax. DSL design is how you stop paying it.

> *The analyst writes tools that let a user community write and maintain their own knowledge.*

That sentence is the whole discipline in one line.

---

## References

- Menzies, T. (2016). *Domain-Specific Languages 101*. ASE 2016 lecture notes. https://github.com/txt/ase16/blob/master/doc/dsl.md  
- Hofstadter, D. (1979). *Gödel, Escher, Bach*. Basic Books.  
- Martin, J. (1967). *Design of Real-Time Computer Systems*. Prentice-Hall.  
- Madachy, R. (2008). *Software Process Dynamics*. Wiley-IEEE Press.  
- Flaxman, A. (2013). Compartmental modeling in Python. https://gist.github.com/aflaxman/4121076  
- Geletko, D. & Menzies, T. (2003). Model-based software testing via incremental treatment learning. *NASA Goddard SEW Proceedings*.


