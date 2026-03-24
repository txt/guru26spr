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
<h1 align="center">:cyclone: CSC491/591: How to be a SE Guru <br>NC State, Spring '26 — HW4 rubric</h1>
 
## CSC491 Rubric (Undergrad) — Q0–Q4
 
| # | Task | Marks | To earn full marks |
|---|------|:-----:|--------------------|
| **Q0** | Better Coding | **2** | Finds and fixes at least 3 clumsy idioms with reusable helpers; call sites in the DSL are visibly cleaner |
| **Q1** | Trace Tool | **2** | `p.trace` captures transitions in the `"[event] from -> to"` format; append happens before the tail call so TCO is intact; a `print_trace` helper displays the log after the run |
| **Q2** | Linter | **2** | `lint(rules, initial)` warns about ghost states, dead ends, and unreachable states; runs cleanly on the provided machine with no false positives |
| **Q3** | Guards | **2** | Engine accepts function-valued transitions, calls them with `p`, and uses the returned string; plain string transitions are unaffected; a working stamina-style guard is shown |
| **Q4** | Wildcard Transition | **2** | `"*"` is checked as a fallback before defaulting to stay-put; behaviour is correct when `"*"` is absent; student identifies the changed line in `fsm2.lua` |
 
---
 
## CSC591 Rubric (Grad) — Q0–Q5
 
| # | Task | Marks | To earn full marks |
|---|------|:-----:|--------------------|
| **Q0** | Better Coding | **1** | Finds and fixes at least 3 clumsy idioms with reusable helpers; call sites in the DSL are visibly cleaner |
| **Q1** | Trace Tool | **2** | `p.trace` captures transitions in the `"[event] from -> to"` format; append happens before the tail call so TCO is intact; a `print_trace` helper displays the log after the run |
| **Q2** | Linter | **2** | `lint(rules, initial)` warns about ghost states, dead ends, and unreachable states; runs cleanly on the provided machine with no false positives |
| **Q3** | Guards | **2** | Engine accepts function-valued transitions, calls them with `p`, and uses the returned string; plain string transitions are unaffected; a working stamina-style guard is shown |
| **Q4** | Wildcard Transition | **1** | `"*"` is checked as a fallback before defaulting to stay-put; behaviour is correct when `"*"` is absent; student identifies the changed line in `fsm2.lua` |
| **Q5** | DOT Exporter | **2** | `to_dot(rules)` produces valid DOT syntax covering all states and transitions; output renders without errors via `dot -Tpng`; gracefully skips states with no transitions |
