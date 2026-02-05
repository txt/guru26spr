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

# HW2B Grading Rubric (10 Points Total)

## Instructions for Graders
This rubric uses a split scoring system to ensure both Undergraduate (UG) and Graduate (G) totals equal **10.0 points**.

- **UG (CSC491):** Use the **UG Pts** column. Skip questions marked "N/A".
- **Grad (CSC591):** Use the **Grad Pts** column. All questions are mandatory.
- **Code Inspection:** As there are no screenshots, grade based on the source code logic, syntax, and implementation of requirements.

---

## Part A: AWK
*(UG Total: 4.5 pts | Grad Total: 4.0 pts)*

| Question | UG Pts | Grad Pts | Description |
| :--- | :---: | :---: | :--- |
| **A1** | 0.50 | 0.25 | Filter Class |
| **A2** | 0.50 | 0.25 | Class Counts |
| **A3** | 0.50 | 0.25 | Most Common Value |
| **A4** | N/A | 0.50 | Cross-tabulation (Grad Only) |
| **A5** | 0.50 | 0.25 | Row Logic & Next |
| **A6** | 1.00 | 0.50 | Entropy Function |
| **A7** | N/A | 0.50 | Reservoir Sampling (Grad Only) |
| **A8** | 0.75 | 0.50 | Naive Bayes Accuracy |
| **A9** | 0.75 | 0.50 | Command Line Variables |
| **A10** | N/A | 0.50 | Laplace Smoothing (Grad Only) |

### Detailed Criteria

**A1. Filter Class**
- [ ] Code includes a pattern match or conditional (e.g., `/diaporthe-stem-canker/` or `$NF == "..."`).
- [ ] Code correctly prints the matching lines (default action or explicit `print`).

**A2. Class Counts**
- [ ] Code uses an associative array (e.g., `count[$NF]++`) to track frequencies.
- [ ] `END` block iterates through the array and prints the class name and count.

**A3. Most Common Value**
- [ ] Logic correctly iterates through Column 2 values to track the maximum frequency.
- [ ] Code prints the specific value and its count in the `END` block.

**A4. Cross-tabulation (Grad Only)**
- [ ] Code tracks counts using a multi-dimensional key (e.g., `count[$NF, $1]++`).
- [ ] Nested loops in the `END` block iterate over classes and values to print the required format `class value count`.

**A5. Row Logic & Next**
- [ ] Logic explicitly handles `NR <= 10` (prints unconditionally).
- [ ] Logic checks `NR > 10` AND `Column 3 != "?"` before printing.
- [ ] The `next` keyword is used to correctly flow between these states.

**A6. Entropy Function**
- [ ] A function `entropy(arr, n)` is defined in the file.
- [ ] The mathematical implementation matches `-sum(p * log(p))` logic.
- [ ] The function is called in the `END` block to print the result.

**A7. Reservoir Sampling (Grad Only)**
- [ ] Code calls `srand()` to ensure randomization.
- [ ] Logic implements reservoir sampling (e.g., `if (rand() < k/n) replace...`) or equivalent random sort logic to select 20 items.

**A8. NB Accuracy**
- [ ] The Naive Bayes script contains a counter for correct predictions vs total rows.
- [ ] The `END` block calculates `correct/total` and includes a print statement for the percentage.

**A9. Command Line Variables**
- [ ] The script uses a variable (e.g., `wait`) that is expected to be passed via `-v` (not hardcoded to 10).
- [ ] The logic uses this variable to control the training/testing split threshold.

**A10. Laplace Smoothing (Grad Only)**
- [ ] Code references `k` and `m` variables (passed via command line).
- [ ] Probability calculation numerators use `+ k`.
- [ ] Probability calculation denominators use `+ k * Attr[i]`.
- [ ] Prior probability logic uses `m` and `NumClasses` correctly: `(Classes[c] + m) / (Total + m * NumClasses)`.

---

## Part B: Lua via Python
*(UG Total: 2.5 pts | Grad Total: 3.0 pts)*

*Note: This section grades the written text file `partB.txt`.*

| Question | UG Pts | Grad Pts | Description |
| :--- | :---: | :---: | :--- |
| **B1** | 0.50 | 0.50 | Metatables vs `__getattr__` |
| **B2** | 0.50 | 0.25 | Function Signatures |
| **B3** | 0.50 | 0.25 | Variance Algorithms |
| **B4** | 0.50 | 0.50 | Modules |
| **B5** | 0.50 | 0.50 | Enumeration |
| **B6** | N/A | 0.25 | List Comprehensions (Grad Only) |
| **B7** | N/A | 0.25 | Max Helper (Grad Only) |
| **B8** | N/A | 0.50 | Type Checking (Grad Only) |

### Detailed Criteria

**B1. Metatables**
- [ ] Explains that Lua's `__index` in a metatable is the mechanism that intercepts lookups for missing keys, exactly like Python's `__getattr__`.

**B2. Function Signatures**
- [ ] Identifies that `d` (after the whitespace gap) is a **local variable**, not a parameter.
- [ ] Provides valid Python equivalent (e.g., `def add(i: int, v: float) -> None:`).

**B3. Variance Algorithms**
- [ ] Identifies Lua uses **Incremental (Welford's)** update, while Python uses **Batch** calculation.
- [ ] Provides a valid reason for preference (e.g., "Incremental is better for streaming/memory" or "Batch is simpler to write").

**B4. Modules**
- [ ] Explains that `return { ... }` at the end of the file exports the table as a module.
- [ ] Compares this to Python's `import` mechanism or `__all__` list.

**B5. Enumeration**
- [ ] Identifies `pairs()` or `ipairs()` as the Lua mechanism to get `index, value`.
- [ ] Notes that Lua iteration *always* provides the key/index, so a specific `enumerate()` function isn't required like in Python.

**B6. List Comprehensions (Grad Only)**
- [ ] Correctly notes Lua lacks list comprehension syntax.
- [ ] Identifies the standard `for` loop appending to a table as the equivalent pattern.

**B7. Max Helper (Grad Only)**
- [ ] Provides Python code that iterates dictionary keys, tracks the `max_val` seen so far, and returns the best key.

**B8. Type Checking (Grad Only)**
- [ ] Explains Python's `match/case` checks structural types or classes (`isinstance`).
- [ ] Explains Lua checks primitive types (`type()`) or metatable strings (`__tostring` or tags).

---

## Part C: First-Class Functions
*(UG Total: 3.0 pts | Grad Total: 3.0 pts)*

*Note: Grade the `fp.lua` source code.*

| Question | UG Pts | Grad Pts | Description |
| :--- | :---: | :---: | :--- |
| **C1** | 0.75 | 0.50 | Collect (Map) |
| **C2** | 0.75 | 0.50 | Select (Filter) |
| **C3** | 0.75 | 0.50 | Reject (Filter Not) |
| **C4** | 0.75 | 0.50 | Inject (Reduce) |
| **C5** | N/A | 0.50 | Detect (Find) (Grad Only) |
| **C6** | N/A | 0.50 | Range Iterator (Grad Only) |

### Detailed Criteria

**C1. Collect (Map)**
- [ ] Function creates and returns a **new** table.
- [ ] Code iterates input and inserts result of `f(v)` into the new table.
- [ ] File includes a test call (e.g., `print(table.concat(collect(...)))`).

**C2. Select (Filter)**
- [ ] Function creates and returns a **new** table.
- [ ] Code checks `if f(v)` before inserting into the new table.

**C3. Reject (Filter Not)**
- [ ] Function creates and returns a **new** table.
- [ ] Code checks `if not f(v)` (or equivalent logic) before inserting.

**C4. Inject (Reduce)**
- [ ] Function signature includes an accumulator (initial value).
- [ ] Loop updates the accumulator at every step using `f(acc, v)`.
- [ ] Returns the final accumulator value.

**C5. Detect (Grad Only)**
- [ ] Loop applies `f(v)` and immediately returns `v` upon the first true result.
- [ ] Returns `nil` (implicit or explicit) if the loop completes without a match.

**C6. Range Iterator (Grad Only)**
- [ ] The function returns a **function/closure** (not a table).
- [ ] The closure properly updates internal state (current value) on each call.
- [ ] Code includes a test loop: `for x in range(...) do ... end`.

---

## Final Score Calculation

| Section | Undergrad Score | Grad Score |
| :--- | :--- | :--- |
| **Part A** | ______ / 4.5 | ______ / 4.0 |
| **Part B** | ______ / 2.5 | ______ / 3.0 |
| **Part C** | ______ / 3.0 | ______ / 3.0 |
| **TOTAL** | **______ / 10.0** | **______ / 10.0** |
