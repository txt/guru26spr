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



# Vibe Coding: Building Software in the Age of LLMs

**CSC 491/591: How to be a SE Guru — Guest Lecture (Amirali Rayegan)**
**NC State University, Spring 2026**

---

## Part 1: Concepts

---

### 1. What Is Vibe Coding?

The term was coined by Andrej Karpathy in February 2025:

> *"There's a new kind of coding I call 'vibe coding', where you fully give in to the vibes, embrace exponentials, and forget that the code even exists."*

In practice, vibe coding means:

- Describing **what you want** in natural language
- Letting an LLM (Claude, Cursor, Copilot, etc.) generate the implementation
- Iterating through conversation rather than through manual edits
- Accepting, steering, and sometimes rejecting what the AI produces

This is not a trick or a shortcut. It is a **fundamental shift in the interface between human intent and running code.**

The question is not *"is vibe coding real?"* — it obviously is. The question is: **what does it mean to be a guru when anyone can vibe code?**

---

### 2. A Brief History of Abstraction

Software engineering has always been about raising the level of abstraction:

| Era | You wrote | You thought in |
|---|---|---|
| 1950s | Machine code | Bits and registers |
| 1960s–70s | Assembly, then C | Memory and control flow |
| 1980s–90s | OOP (Java, C++) | Objects and interfaces |
| 2000s–10s | Frameworks, DSLs | Components and services |
| 2020s+ | Natural language | Intent and outcomes |

Each transition created panic — *"real programmers don't use compilers"* — and each transition **elevated the floor** of what was possible while **raising the ceiling** for those who understood the abstractions beneath.

Vibe coding is the latest rung. The ladder did not disappear.

---

### 3. What Actually Changes

#### What gets easier
- Boilerplate and scaffolding: near-instant
- Translating between languages and frameworks
- Writing tests for known behavior
- Exploring unfamiliar APIs or libraries
- First drafts of documentation

#### What does NOT get easier
- Knowing **what to build** in the first place
- Validating that the generated code is **correct, secure, and maintainable**
- Architectural decisions that compound over time
- Debugging subtle, emergent failures
- Knowing when the AI is confidently wrong

#### The new bottleneck
The bottleneck is no longer *writing code*. It is **reading, evaluating, and steering code you did not write**. The guru's edge shifts from production speed to **judgment**.

This is a return to something old: the senior engineer who doesn't write the most code, but whose comments in code review matter most.

---

### 4. The Principles — What Survives and What Transforms

You've spent this semester with the classics. Here's each one through the vibe coding lens.

---

#### DRY (Don't Repeat Yourself)
**Classic meaning:** One source of truth. Duplication is a maintenance liability.

**In vibe coding:** LLMs are stateless and love to repeat themselves. Ask Claude to add a feature to three files and it may re-implement the same helper three times without noticing. DRY is now *your* job to enforce.

> **Guru move:** After generating a feature, audit for duplication. Prompt: *"Review this code for repeated logic and suggest consolidations."*

---

#### YAGNI (You Aren't Gonna Need It)
**Classic meaning:** Don't build features you don't need yet.

**In vibe coding:** LLMs are trained to be helpful and comprehensive. They will add logging, error handling, configuration flags, and extensibility hooks you never asked for. Generated code is frequently over-engineered by default.

> **Guru move:** Trim the output. Your job shifts from *adding* to *subtracting*. YAGNI becomes an editing discipline, not just a design one.

---

#### Separation of Concerns
**Classic meaning:** Each module should do one thing. UI, logic, and data should not be tangled.

**In vibe coding:** LLMs generating full-stack code will happily mix database calls into your React components, embed business rules in CSS handlers, and place config inside utility functions. They optimize for *working code*, not clean architecture.

> **Guru move:** Give the AI an architecture first. Describe the layers before asking it to fill them. *"Write a pure data-fetching function, nothing else"* outperforms *"write a component that fetches and displays data."*

---

#### VITAL (Vital Infrastructure, Take And Load it locally)
**Classic meaning:** Own your critical infrastructure. Lightweight, local, portable. Don't depend on things you can't control.

**In vibe coding:** The irony is that vibe coding is entirely dependent on external APIs, network calls, and vendor-controlled models. Every prompt is a dependency you don't own.

> **Guru move:** Vibe coding is great for *building*. Your resulting artifact should still honor VITAL. AI-generated code that installs 47 npm packages to do something a shell script could do is still bad code. Review dependency graphs aggressively.

---

#### Complexity Is The Enemy
**Classic meaning:** Simple solutions age better, fail more gracefully, and are understood by more people.

**In vibe coding:** LLMs generate architecturally impressive, syntactically correct, completely over-complicated code — and it *looks* authoritative. The Dunning-Kruger risk is real: code you didn't write feels smarter than it may actually be.

> **Guru move:** If you can't explain what the generated code does, you don't own it yet. The backpacking mindset applies: if you can't carry it, leave it behind.

---

#### Code Review Is Now Mandatory, Not Optional
**Classic meaning:** Peer review catches bugs and spreads knowledge.

**In vibe coding:** There is no peer on the other end. You are reviewing AI output — code that has no ego and no defensiveness, but also no accountability and no memory of the project's history.

> **Guru move:** Treat every generation as a pull request from a very fast, very confident, context-free contractor. Approve nothing you haven't read.

---

### 5. The New Skills of the SE Guru

The guru in 2026 is distinguished not by typing speed but by:

1. **Prompt precision** — Specifying constraints clearly upfront: language, style, dependencies, architecture, edge cases. Garbage in, garbage out still applies.

2. **Skeptical acceptance** — The reflex to verify before shipping. LLMs hallucinate library functions, invent API endpoints, and mis-remember recent changes.

3. **System thinking** — Seeing how the generated piece fits the whole. LLMs see only a context window. You see the full system.

4. **Taste** — Knowing good code when you read it, regardless of who (or what) wrote it. This is irreplaceable. It is built by reading thousands of lines of code written by humans who cared.

5. **Knowing when NOT to vibe** — Security-sensitive code, financial calculations, concurrency logic. Some things require you to think, not just prompt.

---

### 6. The Uncomfortable Truth

Vibe coding will replace a significant fraction of what junior and mid-level programmers currently do. This is already happening.

But there is a category of work that becomes *more* valuable, not less:

- The engineer who writes the **right prompt** because they understand the domain deeply
- The engineer who catches the subtle **logical error** in generated code
- The engineer who maintains the **architectural vision** across a codebase growing faster than ever
- The engineer who can **explain the system** to anyone — human or AI

The guru is not the person who codes the fastest. The guru is the person whose **judgment is the bottleneck** — the one the team, and the AI, needs to get the answer right.

That's what this course is building. It's more relevant now than it has ever been.

---

## Part 2: Live Build — Static Personal Website

We will build a polished, single-file static personal website from scratch using Claude and Cursor — the kind a CS grad student or early-career engineer would actually use.

**Constraints we'll enforce:**
- Single HTML file (VITAL + YAGNI)
- No npm, no build step, no frameworks
- Mobile responsive
- Deployable to GitHub Pages

Watch for where the AI helps, where it over-reaches, and where SE judgment is the difference between shipping something good and shipping something that just runs.

---

### Prompts Cheat Sheet

| Goal | Prompt Pattern |
|---|---|
| Start clean | *"Write X with these constraints: [list]. No [Y], no [Z]."* |
| Audit for DRY | *"Find all repeated logic in this file and suggest consolidations."* |
| Enforce SoC | *"Refactor this so [concern A] is fully separated from [concern B]."* |
| Trim YAGNI | *"Remove everything not required by [spec]. Explain each removal."* |
| Debug precisely | *"On [viewport/condition], [symptom]. Here is the relevant code: [paste]."* |
| Verify before ship | *"What assumptions does this code make that could fail in production?"* |
| Accessibility | *"Review for WCAG AA compliance. List issues by severity."* |

---

## Further Reading

- Karpathy, A. (2025). *"Vibe Coding"* — original Twitter/X post, February 2025
- Menzies, T. — Course notes, CSC 491/591, NC State, Spring 2026
- Brooks, F. (1987). *"No Silver Bullet"* — still right
- Fowler, M. *"Refactoring"* — now applies to AI output too
- SQLite design philosophy — the original backpacking manifesto
