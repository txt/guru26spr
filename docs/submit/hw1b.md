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

I'll create a practical 10-point rubric for grading this refactoring homework.

```markdown
# HW1 Grading Rubric (10 Points Total)

## 1. Functional Correctness (2 points)
- **2 pts**: Reading the code, it seems to produces identical output to wc0.py
- **1 pt**: Reading the code, it seems to produce correct counts but formatting differs slightly
- **0 pts**: Reading the code, it looks like it produces incorrect output or won't run

## 2. Separation of Concerns - SoC (2 points)
- **2 pts**: Clean separation of model (word counting logic) from I/O (file reading, printing)
  - Model functions return data structures (no printing)
  - Presentation layer handles all output formatting
- **1 pt**: Partial separation (some mixing remains)
- **0 pts**: Model and I/O still intertwined

## 3. Single Responsibility Principle - SRP (2 points)
- **2 pts**: Each function does ONE clear job
  - Word cleaning is separate from counting
  - Counting is separate from filtering
  - File reading is separate from processing
- **1 pt**: Most functions focused, but 1-2 still do multiple jobs
- **0 pts**: Functions still doing multiple unrelated tasks

## 4. Mechanism vs Policy (1 point)
- **1 pt**: Policies extracted to CONFIG/data structure
  - Stopwords in data (not hardcoded in logic)
  - Top N count configurable
  - Punctuation rules extractable
- **0.5 pts**: Some policies extracted
- **0 pts**: Policies still hardcoded in functions

## 5. Small Functions (1 point)
- **1 pt**: No function exceeds ~10-12 lines of actual code
- **0.5 pts**: Most functions small, 1-2 slightly longer
- **0 pts**: Multiple large functions remain

## 6. Documentation & Comments (2 points)
- **2 pts**: Excellent commenting
  - Clear Q1, AQ1, Q2, AQ2, Q3, AQ3, Q4, AQ4 markers
  - Explains WHAT heuristic each section addresses
  - Explains WHY the refactoring improves design
- **1 pt**: Has required markers but explanations are superficial
- **0 pts**: Missing markers or minimal comments

---

## Bonus Points (Optional, up to +2)

- **+0.5**: Multiple output formats (JSON, CSV, etc.)
- **+0.5**: Load stopwords from external file
- **+0.5**: Unit tests included
- **+0.5**: Additional insights or creative improvements

---

## Quick Grading Checklist:

**Functional (2 pts)**
- [ ] REading he code, looks like same output as original?

**SoC (2 pts)**  
- [ ] Model functions return values (no print)?
- [ ] I/O separated from logic?

**SRP (2 pts)**
- [ ] ~10+ focused functions?
- [ ] Each does one clear thing?

**Mechanism/Policy (1 pt)**
- [ ] CONFIG dict present with policies?

**Small Functions (1 pt)**
- [ ] All functions ≤10-12 lines?

**Comments (2 pts)**
- [ ] Q1-Q4 and AQ1-AQ4 markers present?
- [ ] Explains what/why for each heuristic?

---

## Grading Notes:

**Common Issues to Watch For:**
- Functions that still print AND return values (-SoC)
- `main()` function > 15 lines (-SRP, -Small)
- Stopwords hardcoded in counting logic (-Policy)
- Missing explanatory comments (-Documentation)

**Excellence Indicators:**
- Clean data flow: read → process → format → display
- Functions compose well together
- Easy to add new features (formats, languages)
- Comments show understanding of *why* each heuristic matters
```

This rubric emphasizes the core learning objectives while being practical to apply consistently. Want me to adjust the point distribution or add any specific criteria?
