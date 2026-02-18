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

# The Architecture of Understanding: A Masterclass in Documentation

As AI and cognitive researcher David Leake [^leake]
observed, explanation is not a passive
dump of facts. It is an active inference procedure in its own right. A useful
explanation must be dynamically tuned to the specific goals, anomalies, and prior
knowledge of the audience. Documentation is exactly this: an active cognitive bridge
between the machine's logic and the human's mental model.

[^leake]: Leake, D. B. (1992). *Evaluating Explanations: A Content
Theory*. Lawrence Erlbaum Associates. Leake's research emphasizes
that explanation is a goal-driven cognitive process meant to resolve
specific anomalies for a specific actor, rather than a one-size-fits-all
data dump.


[^github]: GitHub. (2021). [*Octoverse Report*](https://octoverse.github.com/2021/)
The Octoverse report states that developers see a 50% productivity boost when they have access to easy-to-source, up-to-date, and reliable documentation.


According to a 2022 GitHub survey[^github], developers spend over 50% of their time reading
code and documentation, compared to writing new code. Poor documentation is cited
as the #1 cause of lost productivity, costing teams hours per week in reverse
engineering.

Writing good documentation is not a tax on development; it is an investment in
future velocity. But where do you start? How do you tune your inference procedure
to the audience?

## Diataxis


We will use the **Diátaxis Framework**.
as created by Daniele Procida, a tech industry veteran, former philosophy student, and core contributor to the Python Django web framework. While working at the software company Divio and managing Django's extensive open-source documentation, Procida noticed a recurring problem: developers treated documentation as a monolithic data dump. Authors were constantly mixing concepts, instructions, and facts into the same articles, resulting in documentation that was confusing to read and impossible to maintain. He first formalized his solution in a highly influential 2017 PyCon AU talk titled *"What nobody tells you about documentation,"* which he later refined into the comprehensive Diátaxis (from the Ancient Greek *dia* "across" and *taxis* "arrangement") framework.

At its theoretical core, Diátaxis is based on the philosophy of *craft* and *skill*. Procida argued that documentation exists solely to serve a user who is trying to master or apply a craft (like programming). If you analyze human skill, it exists across two intersecting cognitive dimensions:

1. **Action vs. Cognition:** Are we doing something practical (*knowing how*), or are we thinking about something theoretical (*knowing that*)?
2. **Acquisition vs. Application:** Are we in the process of learning the skill (studying), or are we actively using the skill to get real work done (applying)?

When you intersect these two dimensions, you create a complete 2x2 map of human cognitive needs. Because these two dimensions entirely define the territory of "craft," Procida argues there are exactly—and only—four types of documentation:

* **Acquisition + Action = Tutorials** (Learning by doing)
* **Application + Action = How-T Guides** (Applying skills to a specific task)
* **Application + Cognition = Reference** (Looking up facts while working)
* **Acquisition + Cognition = Explanation** (Deepening theoretical understanding)

By understanding this theory, you realize that mixing documentation types isn't just a stylistic error; it is a cognitive mismatch that forces the reader's brain to violently switch between learning, doing, and theorizing.

Diátaxis divides documentation into four distinct quadrants based on user needs:
1. **Reference** (Information-oriented: "What is this?")
2. **How-To Guides** (Task-oriented: "How do I do this specific thing?")
3. **Tutorials** (Learning-oriented: "Teach me the basics.")
4. **Explanation** (Understanding-oriented: "Why is it designed this way?")

Your goal by the end of this lecture is to master all four, utilizing LLMs as
your co-writer, and to know exactly when to deploy each type based on your
audience's goals.

---

## 1. REFERENCE: The Micro-Level (Type Hints & Docstrings)

Reference material is information-oriented. It assumes the user knows what they
want to achieve but needs the exact technical specifications.

**What are Type Hints?**
Introduced in Python 3.5 (PEP 484), type hints are annotations that explicitly
declare the expected data types of variables, arguments, and return values.
They do not change how the code runs. Instead, they act as machine-readable
documentation for IDEs, static analysis tools (like `mypy`), and developers.

**A) Sample: Raw Code vs Custom Types & Hints**
Here is raw, undocumented code from our multi-objective optimizer, [xai.py](xai.py):

```python
def norm(num, n):
    if n == "?": return 0.0
    z = (float(n) - num.mu) / sd(num)
    z = max(-3, min(3, z))
    return 1 / (1 + exp(-1.7 * z))

```

To document this, we first define our own *convenience types* (type aliases) to
make our signatures readable. Then we add output types, disjunctions (using the
`|` operator for "or", introduced in Python 3.10), and docstrings:

```python
from types import SimpleNamespace
from typing import Any, Iterable, Optional

# 1. Define custom convenience types to simplify signatures
Qty = int | float          # Disjunction: A quantity is an int OR a float
Row = list[Qty | str]      # A row is a list containing Qty or strings
Obj = SimpleNamespace      # Alias for our base object structure

# 2. Apply type hints to inputs and define the output type (-> float)
def norm(num: Obj, n: Qty | str) -> float:
    """Normalizes a number using a logistic function to handle outliers."""
    if n == "?": return 0.0
    z = (float(n) - num.mu) / sd(num)
    z = max(-3, min(3, z))
    return 1 / (1 + exp(-1.7 * z))

```

**B) Structure of Reference Docs**

* **Goal:** Accurate, complete, and austere descriptions.
* **Components:** Parameter lists, return types, custom aliases, and exceptions.
* **Rule:** Do not teach concepts here. Just state the facts.
* **Interesting Types to Know (from the `typing` module):**
* `Any`: The ultimate escape hatch. Accepts literally any data type.
* `Optional[type]`: Shorthand for `type | None`. Great for default arguments.
* `Iterable[type]`: Anything you can loop over (lists, sets, generators).



**C) The LLM Prompt**

> "Act as a strict technical writer. Analyze the following Python function.
> Define any necessary custom type aliases (like `Qty` for `int | float`) to
> keep the signature clean. Return the function rewritten with PEP-484 compliant
> type hints (including return types and disjunctions) and a Google-style docstring."

```python
def go_tree_score(d, lo, mid):
  return int(100*(1- (d - lo)/ (mid - lo + 1/BIG)))
```

**D) Exercise: Run & Comment**

1. Run the prompt above on the `treeGrow` function from [xai.py](xai.py)
2. *Comment on the result:* Did it use `Any`, or did it successfully guess the parameter types?
You must always review generated types to ensure the AI didn't hallucinate
overly restrictive limits (e.g., forgetting that a number could be a float
or an unknown string like `?`).

----

## 2. REFERENCE: The Macro-Level (Auto-Generating Docs with `pdoc`)

While type hints document individual lines, your users need a searchable map of
your entire codebase. This is where tools like `pdoc` or `Sphinx` come in.


**A) Sample: The Role of Auto-Generated Docs**
`pdoc` reads your Python files, extracts all functions, type hints, and
docstrings, and turns them into a standalone HTML website. In Diátaxis, this
maps *exactly* to the **Reference** quadrant because its structure is dictated
by the code's architecture, not by the user's learning journey.

**B) Write By Hand: Generating the Docs**
You don't write the HTML by hand; you generate it. However, you *do* manually
write the module-level docstrings that `pdoc` parses. A common mistake is
shoving a "Tutorial" or "How-To" into the top of a Python file. Reference docs
must remain strictly informational.

**C) Ask for LLM Support**
> "Analyze the module-level docstring at the top of `xai.py`. Evaluate it
> strictly against the Diátaxis 'Reference' quadrant. Identify any instructions
> or tutorials that do not belong in pure Reference. Rewrite the docstring to
> be an austere, code-focused Reference summary suitable for `pdoc`."

**D) Exercise: Run & Critique**
1. Run this command in your terminal to generate the docs:
   `pdoc -o ~/tmp --force --html xai.py ; open ~/tmp/xai.html`
2. *Critique using Diátaxis:* Look at the generated webpage.
   - Does this page help a beginner learn the concepts (Tutorial)?
   - Does it help them accomplish a specific task (How-To)?
   - Does it explain the architectural philosophy (Explanation)?


---

## 3. HOW-TO GUIDES: The Task Level (UNIX man pages)

To understand the next bit,   we have to look back
to the early 1970s at Bell Labs. When Ken Thompson and Dennis Ritchie were
first building UNIX, they established a radical cultural mandate: a program did
not truly exist until it was documented. This culminated in November 1971 with
the publication of the first *UNIX Programmer's Manual*. It wasn't a sprawling,
conversational textbook; it was a collection of stark, highly structured, and
ruthlessly efficient technical recipes designed to help a programmer accomplish
a specific task from the terminal. We know these today as "man pages."

What made Bell Labs' approach revolutionary was not just *what* they wrote, but
*how* they wrote it. They did not use traditional word processors. Instead,
they invented the concept of "Documentation as Code." The manuals were written
in plain text with embedded formatting macros and compiled using typesetting
programs called `roff`, `nroff`, and later `troff`. The documentation lived in
the same file system, was edited with the same text editors, and was compiled
with the same build tools as the C code it was describing.

By the late 1970s, this documentation pipeline had become so powerful and widely
used—even by the Bell Labs patent department—that AT&T spun it off as a standalone
commercial product called the UNIX Documenter's Workbench (DWB). DWB was an
architectural marvel. Rather than building a monolithic word processor, it
relied on the UNIX philosophy of small, composable tools. It included domain-
specific micro-languages: `eqn` for compiling mathematical equations, `tbl` for
generating tables, and `pic` for drawing diagrams.


The legacy of DWB and the man page is the realization that documentation is an
engineering discipline in its own right. A UNIX man page sits perfectly on the
border of the Diátaxis **Reference** and **How-To** quadrants. It provides the
austere facts (flags, arguments, file formats), but it is ultimately structured
around *action*—getting the user to successfully execute a command.

When we write our own command-line tools today, we still emulate this exact
structure. A How-To guide is goal-oriented. The user is in the middle of a
project, the terminal is open, and they need a recipe to complete a specific
task right now.


**A) Sample: UNIX `groff` man page (`xai.1`)**

Example: [xai.pdf](xai.pdf). Generated from [xai.1](xai.1).
```groff
.TP
.BI \-b " bins"
Set the number of bins for discretizing continuous values. Default is \fB7\fR.

```

Try this yourself:

-   Man to pdf: `groff -man -Tps xai.1 | ps2pdf - xai.pdf`
- Man to plain text: `groff -man -Tutf8 xai.1 | col -bx > xai_clean.txt`
- Man to html: `groff -man -Thtml xai.1 > xai_manpage.html`
  - Hideous 1998 style html. We will do better below. See pandoc.

**B) Structure of a How-To**

* **Goal:** Solve a specific problem sequentially.
* **Components:** Prerequisites, numbered steps, expected output.
* **Rule:** Omit unnecessary explanations. Get the user to the finish line.

**C) The LLM Prompt**

> "I have a Python script `xai.py` that accepts a `--tree` flag to run a
> decision tree optimizer on a CSV. Generate a groff-style man file for that doc.
> Include notes on the data format use in the csv as well as a few usage
> example."

**D) Exercise: Run & Comment**

1. Execute the prompt.
2. *Comment on the result:* Did the LLM include steps to download the CSV first?
A good How-To must not skip implicit steps. If the AI missed it, manually add:
"Step 1: Download auto93.csv".

---

## 4. MODERNIZING THE PIPELINE: The Pandoc Transpiler

While Bell Labs' `groff` is historically profound, running `groff -Thtml` 
produces web pages that look like they belong in 1996. The HTML lacks 
mobile responsiveness, uses deprecated inline styling, and is difficult 
to parse with modern CSS. 

Enter **Pandoc**. Created by philosophy professor John MacFarlane, Pandoc 
is the "Swiss Army knife" of document conversion. Unlike simple regex 
scripts that just replace text tags, Pandoc acts as a true compiler for 
human languages. It parses your input document into an Abstract Syntax Tree 
(AST) in memory, and then transpiles that AST into almost any output 
format imaginable.


If you want to bring legacy UNIX man pages into the modern era, Pandoc 
is the industry standard. It reads the archaic `groff` macros and transpiles 
them into clean, semantic tags. 

**Sample: Pandoc File Format Transpilers**
The basic syntax is `pandoc [input] -s (standalone) -o [output]`. Pandoc 
usually guesses the formats from the file extensions, but you can explicitly 
force the parsers using `-f` (from) and `-t` (to).

**1. Man page to Plain Text**
Strips out all the legacy backspace formatting and leaves clean ASCII/UTF-8.
```bash
pandoc xai.1 -f man -t plain -o xai_modern.txt

```

**2. Man page to Modern HTML5**
Produces clean, semantic `<header>`, `<section>`, and `<dl>` tags that are
ready to be styled with modern CSS frameworks. The `-s` flag ensures it
builds a complete HTML file, not just a snippet.

```bash
pandoc xai.1 -s -f man -t html -o xai_modern.html

```

**3. Man page to PDF**
Pandoc uses LaTeX under the hood to generate gorgeous, textbook-quality PDFs
from your raw terminal man pages. *(Note: Requires a LaTeX engine like
`pdflatex` or `xelatex` installed on your system).*

```bash
pandoc xai.1 -s -f man -o xai_modern.pdf
```

---

## 5. SCALING UP (1):  PANDOC

For this example, we'll need "tectonic"

Windows people, in an empty directory:

```
curl --proto '=https' --tlsv1.2 -fsSL https://drop-sh.fullyjustified.net | sh
sudo mv tectonic /usr/local/bin/

```

Everyone else

```
brew install tectonic # Mac
curl --proto '=https' --tlsv1.2 -fsSL https://drop-sh.fullyjustified.net | sh # LINUX

```

You will need the files

- [slides.md](slides.md)
- [logo.png](logo.png)
- [head.pdf](head.pdf)

```
pandoc -o ~/tmp/slides.pdf slides.md -t beamer --pdf-engine=tectonic
```

That is how to move markdown to slides? But how to generated the markdown?

```
Please convert the provided LaTeX manuscript (`main.tex`) and its bibliography (`refs.bib`) into a Markdown presentation slide deck suitable for Beamer/Pandoc conversion.

Act as an expert academic presenter summarizing a paper into a concise, engaging conference presentation.

Follow these strict formatting and structural rules based on my existing templates:

1.  **YAML Frontmatter**: Start the file with the exact YAML metadata block below, updating the `title`, `subtitle`, `author`, `institute`, and `date` to match the metadata from `main.tex`. Preserve the theme, colortheme, and all `header-includes`.
    ```yaml
    ---
    title: |
       [Insert Paper Title Here]\
       [Insert subtitle/second line if needed]
    subtitle: ([Insert short hook or subtitle])
    author: [Insert Author Names]
    institute: |
      [Insert Affiliation details, formatted with \\ and line breaks]
    date: [Insert Date or Conference Event]
    slide-level: 2
    fontsize: 9pt
    theme: Warsaw
    colortheme: default
    header-includes:
      - \titlegraphic{\vspace{-5mm}\includegraphics[height=3cm]{logo.png}}
      - \usepackage[sfdefault,light]{FiraSans}
      - \usepackage{microtype}
      - \definecolor{LogicBlue}{RGB}{204,0,0}
      - \definecolor{InferenceRed}{RGB}{212,55,59}
      - \definecolor{linkblue}{HTML}{0066FF}
      - \definecolor{myred}{HTML}{CC0000}
      - \setbeamercolor{structure}{fg=InferenceRed}
      - \setbeamercolor{frametitle}{bg=LogicBlue,fg=white}
      - \setbeamercolor{palette primary}{bg=LogicBlue,fg=white}
      - \setbeamercolor{palette secondary}{bg=InferenceRed,fg=white}
      - \setbeamertemplate{navigation symbols}{}
      - \hypersetup{colorlinks=true,urlcolor=linkblue}
      - \setbeamertemplate{footline}{\hspace*{.83cm}\insertframenumber/\inserttotalframenumber\hfill}
    ---
    ```

2.  **Slide Structure**:
    * Use `## Slide Title` for each new slide.
    * Distill the narrative of the `main.tex` paper (which looks back from 2036 at the evolution of SE journals) into 10-15 logical slides.
    * Cover the main themes: The fragmented past, the transition/crisis, the adoption of open infrastructure/AI, and the collaborative present (2036).

3.  **Content Formatting**:
    * **NO walls of text.** Convert long LaTeX paragraphs into concise, punchy bullet points.
    * Use bolding strategically to highlight key terms.
    * Use blockquotes (`>`) for key takeaways or impactful statements.

4.  **References Slide**:
    * Make the final slide `## References`.
    * Extract the top 5-7 most relevant citations from the text/`refs.bib` and format them exactly like this:
        `**[CitationKey]:** First Author *et al.*, "Paper Title," *Venue Name*, Year.`

Output strictly the raw Markdown code for the slides so I can compile it directly.
```

To test this prompt, give an LLM all the *.bib, main.tex. *.png files in [future_se__journals](future_se__journals) and
see what it generates.

---

## 6. TUTORIALS: The Learning Level (Interactive Transcripts)

Tutorials are learning-oriented. The user is a beginner. You must hold their
hand and guide them through a controlled, successful experience.

**A) Sample: The "Dribble" Transcript ([km-overview.script.txt](km-overview.script.txt)**

```lisp
;;; "What is the position [in this new situation] of that switch?"
[_Situation30] KM> (the position of *MySwitch)
(*Up)

```

**B) Structure of a Tutorial**

* **Goal:** Build confidence and impart basic competence.
* **Components:** Narrative flow, safe examples, REPL transcripts (Read-Eval-
Print Loop), and visible system responses.
* **Rule:** The user must succeed. Do not introduce edge cases or errors here.

**C) The LLM Prompt**

> "Act as a beginner exploring the `xai.py` library in an interactive Python
> REPL. Generate a 'dribble transcript' tutorial. Show the Python prompts (>>>),
> the commands to load a CSV into a `Data` object, the printed outputs, and
> include inline comments (###) explaining what is happening."

**D) Exercise: Run & Comment**

1. Generate the REPL transcript using the prompt.
2. *Comment on the result:* Read the output. Does it feel like a real session?
LLMs often hallucinate exact mathematical outputs (like exact standard
deviations). You may need to replace AI-generated numbers with real terminal
output to ensure accuracy.

----

7. SCALING UP (2):   Meta-prompting

The site [xai.html](xai,html) is one file generated via the prompt
[xai.html#about](xai.html#about).

That is:

- I manually fussed around
- I asked the LLM to record the style of my product
- I made changes to the code
- I asked an  LLM to update the doco according to that prompt

 The results are... Intriguing  by exasperating. There are so many small things here I want to change. Would take
    hours. Would I  actually use this to document my yode? Or is it really a tutor helping me to define
    my idea of "good" doco which I would then go away and apply (manually) elsewhere?

---

## 7 EXPLANATION: The Macro Level (Philosophy & Narrative)

Explanation is understanding-oriented. The user wants to know *why* the system
exists, its architectural philosophy, and the history behind its design.

**A) Sample: [unix6.pdf](Lions' Commentary on UNIX V6) / [K&R C](kr,pdf)**

> "The easiest way to vary the main memory space used by the operating system
> is to vary 'NBUF'. If this is forbidden, propose the best way to..."

**B) Structure of an Explanation**

* **Goal:** Provide context and build a mental model.
* **Components:** Analogies, historical context, design trade-offs, limitations.
* **Rule:** Do not include tutorials or task instructions. Focus on the "Why."

**C) The LLM Prompt**

> "Analyze the explanatory style of [k&r](kr.pdf)   Using that
> exact narrative tone, write a checklist for `what is good doco'.

K&R results:


_Scope & promise_
- [ ] State what this chapter will teach (concrete outcomes).
- [ ] State what it will NOT cover yet (and when it appears later).
- [ ] Say if the chapter is intentionally incomplete / a framework.

_Reader onboarding_
- [ ] First page: how to run the thing (build/run/test loop).
- [ ] Show the smallest working example early.
- [ ] Add a "break it on purpose" exercise to teach tool feedback.

_Example strategy_
- [ ] Prefer complete, runnable programs over isolated fragments.
- [ ] Each example has a clear job (one idea + one useful behavior).
- [ ] Examples scale: tiny -> slightly bigger -> reusable pattern.

_Explain order_
- [ ] Whole program first, then explain parts (whole -> parts).
- [ ] Explain names as you introduce them (no forward mystery).
- [ ] Keep explanations local; avoid long detours.

_Readability & style as first-class_
- [ ] Use indentation to reveal control structure.
- [ ] Use meaningful names; replace magic numbers with symbols.
- [ ] Encourage comments where they add understanding.

_Principles from specifics_
- [ ] After an example, generalize a rule-of-thumb.
- [ ] Mention tradeoffs (clarity vs brevity; options and why choose).
- [ ] Point out common smells (magic numbers, hidden assumptions).

_Robustness & boundaries_
- [ ] Call out edge cases early (empty input, off-by-one, etc.).
- [ ] Explain why a construct behaves well (or not) on boundaries.

_Practice & feedback_
- [ ] Exercises prompt edits, experiments, and verification.
- [ ] Exercises are incremental: small changes, visible outcomes.

_Audience support_
- [ ] Offer paths for novices vs experienced readers.
- [ ] Reinforce: "write small programs" as the fastest learning loop.

Lions results:

(Gemini crashed last night)


**D) Exercise: Run & Comment**

1. Take the above 2 check lists. Ask a LLM to turn them into a prompt.
2. Run them to generate help text for [xai.py](xai,py)
2. *Comment on the result:* How ell does it satisy  Diataxis? What extra knowledge is needed


---

## SUMMARY: Rules of Thumb for Documentation

When should you use which? Ask yourself what the user is feeling:

1. **Are they studying the code directly?** -> Write **Reference** (Type hints).
2. **Are they stuck on a specific task?** -> Write a **How-To** (Step-by-step).
3. **Are they completely new here?** -> Write a **Tutorial** (REPL transcript).
4. **Are they evaluating your architecture?** -> Write an **Explanation** (Why).

*Challenge:* Pick one function you wrote this week, and write all four types
of documentation for it. Observe how your brain shifts gears for each one.

