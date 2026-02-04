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

# HW3 Grading Rubric (10 Points Total)

## Instructions for Graders
This rubric uses a split scoring system to ensure both Undergraduate (UG) and Graduate (G) totals equal **10.0 points**.

- **UG (CSC491):** Use the **UG Pts** column. Skip questions marked "N/A".
- **Grad (CSC591):** Use the **Grad Pts** column. All questions are mandatory.

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
- [ ] Output contains **only** lines where the last column is exactly `diaporthe-stem-canker`.

**A2. Class Counts**
- [ ] Output contains a clean list of unique classes followed by their integer counts (e.g., `diaporthe-stem-canker 19`).

**A3. Most Common Value**
- [ ] Correctly identifies the most frequent value in Column 2 (which is either `1`, `0`, or `?`) and prints its specific count.

**A4. Cross-tabulation (Grad Only)**
- [ ] Output follows the format: `class_name value count`.
- [ ] Shows counts for every distinct value in Column 1, grouped by class.

**A5. Row Logic & Next**
- [ ] Rows 1-10 are **always** printed.
- [ ] Rows 11+ are **only** printed if Column 3 is NOT `?`.
- [ ] The code uses the `next` keyword to skip remaining logic for excluded rows.

**A6. Entropy Function**
- [ ] A function `entropy(arr, n)` is clearly defined.
- [ ] The math correctly implements `-sum(p * log(p))` where `p = count/n`.

**A7. Reservoir Sampling (Grad Only)**
- [ ] Output contains exactly 20 lines (excluding header).
- [ ] Uses `srand()` and `rand()`.
- [ ] Running the script twice produces **different** random subsets.

**A8. NB Accuracy**
- [ ] The Naive Bayes script runs without syntax errors.
- [ ] The `END` block prints a final accuracy score (e.g., `Accuracy: 85%`).

**A9. Command Line Variables**
- [ ] The script accepts a variable (e.g., `wait`) via the `-v` flag.
- [ ] The loop limit is not hardcoded to `10`.
- [ ] Changing the argument (e.g., `-v wait=50`) produces a different accuracy result.

**A10. Laplace Smoothing (Grad Only)**
- [ ] Accepts `k` and `m` via command line.
- [ ] Numerator uses `(freq + k)`.
- [ ] Denominator uses `(total + k * Attr[i])`.
- [ ] Prior probability uses `(Classes[c] + m) / (Total + m * NumClasses)`.

---

## Part B: Lua via Python
*(UG Total: 2.5 pts | Grad Total: 3.0 pts)*

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
- [ ] Returns a **new** table (does not modify input in place).
- [ ] Correctly applies the function to every element (e.g., `{1,2,3} -> {1,4,9}`).

**C2. Select (Filter)**
- [ ] Returns a **new** table.
- [ ] Result contains ONLY elements where `func(x)` returns `true`.

**C3. Reject (Filter Not)**
- [ ] Returns a **new** table.
- [ ] Result contains ONLY elements where `func(x)` returns `false`.

**C4. Inject (Reduce)**
- [ ] Function accepts an accumulator.
- [ ] Iterates the list and updates the accumulator using the function (e.g., summing a list).

**C5. Detect (Grad Only)**
- [ ] Returns the **first** element that matches the condition.
- [ ] Returns `nil` if no match is found.

**C6. Range Iterator (Grad Only)**
- [ ] The function returns a **closure/function**, NOT a table/list.
- [ ] The test case iterates successfully (e.g., `for x in range(1,5) do print(x) end`).

---

## Final Score Calculation

| Section | Undergrad Score | Grad Score |
| :--- | :--- | :--- |
| **Part A** | ______ / 4.5 | ______ / 4.0 |
| **Part B** | ______ / 2.5 | ______ / 3.0 |
| **Part C** | ______ / 3.0 | ______ / 3.0 |
| **TOTAL** | **______ / 10.0** | **______ / 10.0** |
