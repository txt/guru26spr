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


# Shell + Make: Automation for Grad Students

## Part 0: Why This Lecture Exists

**1973. Bell Labs. Lee McMahon needs to analyze the Federalist Papers.**
He wants to search authorship patterns across massive text files.
Problem: `ed` loads files into memory. Can't handle it.

McMahon asks Ken Thompson for help. Thompson looks at `ed`'s source code.
**He spends one hour.** Extracts the regex parser from `ed`.
Makes it standalone. Names it after the command `g/re/p`
(global/regular expression/print). Ships it as `grep`.
Becomes Unix legend.

Note: Thompson did not "ship" grep to McMahon. He just added it to his "bin".
Now anyone on the same file system can access grep by adding Ken's path to
their startup:

```sh
export PATH="$PATH:/usr/kenr/bin" # look at kenr's code, last
grep "Madison" federalist.txt | sort | uniq -c
```

### Unix: A Community of Tools

Unix wasn't built for one person. It was built for **many people with
different problems.**

The breakthrough: **decentralized control.**

- Thompson writes `grep` for text search
- Someone else writes `sort` for ordering
- Another writes `uniq` for deduplication
- Shell glues them together

No central planner decided this pipeline. Three people solved three
problems. Shell connected them.

### The Shell Story: Glue, Not Compute

Shell wasn't designed to replace other languages. It was designed to
**connect** them.

Want arithmetic? Hard:
```sh
x=$((5 + 3))    # Modern bash
x=`expr 5 + 3`  # Old way - spawns a process!
```

Want to call Python? Easy:
```sh
python3 -c "print(5 + 3)"
```

**Shell's superpower: orchestrating other programs.**

Originally, even `false` isn't built-in. It's `/usr/bin/false`:

```c
#define EXIT_STATUS EXIT_FAILURE
#include "true.c"
```

That's the entire source. Returns 1. Done.

Shell knows paths. If `PATH` contains `/usr/bin`, this works:
```sh
if false; then echo "never runs"; fi
```

Shell finds `/usr/bin/false`, runs it, checks exit code.
Zero = success. Non-zero = failure.

(Historical note: in newer versions of shells, true/false are built in.)

### Why This Matters

**grep exists because Unix decentralized tool creation.**

Everyone can add to their own `/usr/myname/bin`. Shell finds it. Community
grows.

No permission needed. No central registry. Just:
1. Write a program
2. Put it in `PATH`
3. Everyone can use it

This lecture: you're joining that tradition.

### Your Turn

Build your own tools. Make them small. Ship them.
Let reality tell you what's needed next.

---

## Part 0.5: How to Read Shell Commands

Before we dive in, you need to **decode the syntax**. Shell looks cryptic
until you learn its grammar.

### Variables

```sh
name="Tim"           # Create variable (no spaces around =)
echo $name           # Use it ($ extracts value)
echo "$name"         # Quoted (preserves spaces)
echo '$name'         # Single quotes = literal text
echo "Hi $name!"     # Double quotes = expand variables
```

```
┌─ Reading Guide ────────────────────────────────┐   
│ $var         →  Get variable value             │   
│ "$var"       →  Get value, preserve spaces     │   
│ '$var'       →  Literal text, no expansion     │   
│ var="value"  →  Assign (no spaces around =)    │   
└────────────────────────────────────────────────┘   
```

### Quoting Rules

```sh
file="my document.txt"
cat $file              # WRONG: cat sees "my" and "document.txt"
cat "$file"            # RIGHT: cat sees one file
```

### Command Substitution

```sh
# Capture command output
today=$(date)          # Modern syntax
today=`date`           # Old syntax (avoid)

# Use it
echo "Today is $today"

# Inline
echo "There are $(ls | wc -l) files here"
```

```
┌─ Reading Guide ────────────────────────────────┐   
│ $(command)   →  Run command, capture output    │   
│ `command`    →  Old syntax (harder to nest)    │   
└────────────────────────────────────────────────┘   
```  
### Redirection

```sh
cmd > file             # Overwrite file with output
cmd >> file            # Append output to file
cmd 2> errors.txt      # Redirect errors only
cmd &> all.txt         # Redirect output AND errors
cmd1 | cmd2            # Pipe output to next command
cmd < input.txt        # Read from file
```

```
┌─ TRY THIS ────────────────────────────────────┐
│ echo "Hello" > test.txt                       │
│ echo "World" >> test.txt                      │
│ cat test.txt                                  │
│                                               │
│ What do you see? What's the difference?       │
└───────────────────────────────────────────────┘
```

### Tests and Conditionals

```sh
# Old style (portable but limited)
if [ -f "file.txt" ]; then
  echo "File exists"
fi

# New style (bash/zsh, more powerful)
if [[ -f "file.txt" ]]; then
  echo "File exists"
fi

# Common tests
[[ -f file ]]          # File exists?
[[ -d dir ]]           # Directory exists?
[[ -z "$var" ]]        # Variable empty?
[[ "$a" == "$b" ]]     # Strings equal?
[[ "$a" != "$b" ]]     # Strings not equal?
```

### Exit Codes and Chaining

```sh
# Every command returns a number
true                   # Returns 0 (success)
echo $?                # Shows last exit code: 0

false                  # Returns 1 (failure)
echo $?                # Shows: 1

# Chain commands
cmd1 && cmd2           # Run cmd2 only if cmd1 succeeds
cmd1 || cmd2           # Run cmd2 only if cmd1 fails

# Example
grep -q "TODO" file.txt && echo "Has TODOs" || echo "Clean"
```

What Just Happened?
-------------------
1. grep returns 0 if it finds "TODO", 1 if not
2. && runs next command only on success (0)
3. || runs next command only on failure (non-zero)
4. Result: one echo always runs

### Functions

```sh
# Define
greet() {
  echo "Hello $1"      # $1 = first argument
}

# Call
greet World            # Prints: Hello World
greet "Tim Menzies"    # Prints: Hello Tim Menzies
```

```            
┌─ TRY THIS ────────────────────────────────────┐
│ 1. Type this function:                        │
│    greet() { echo "Hi $1, you are $2"; }      │
│                                               │
│ 2. Call it:                                   │
│    greet Alice awesome                        │
│                                               │
│ 3. What happens with: greet Bob               │
│    (only one argument?)                       │
└───────────────────────────────────────────────┘
```

### Special Variables

```sh
$0         # Script name
$1 $2 $3   # First, second, third arguments
$@         # All arguments (preserves spaces)
$#         # Number of arguments
$?         # Exit code of last command
$$         # Current process ID
```

Example:
```sh
#!/bin/bash
echo "Script: $0"
echo "Args: $@"
echo "Count: $#"
```

Run it:
```sh
bash script.sh apple banana
# Script: script.sh
# Args: apple banana
# Count: 2
```

---

## Part 1: Why Bother?

Typing is expensive. Remembering is expensive. Let's automate.

```sh
# Bad: type this 50 times
python3 -m pydoc -w myfile && mv myfile.html myfile.pdf

# Good: type this once
make pdf
```

Other examples from my daily workflow:

```sh
# Short command
make ~/tmp/mycode.pdf

# Under the hood, in a Makefile
# (so glad I do not have to remember this all the time)
~/tmp/%.pdf: %.py  ~/tmp Makefile ## .py ==> .pdf
	@echo "pdf-ing $@ ... "
	@a2ps               \
		-Br               \
		--quiet            \
		--portrait          \
    --lines-per-page=100  \
		--font-size=6 \
		--line-numbers=1      \
		--borders=no           \
		--pro=color             \
		--columns=2              \
		-M letter                 \
		-o - $< | ps2pdf - $@
	@open $@
```

```
┌─ Reading Guide ────────────────────────────────┐
│ %.pdf: %.py  →  Pattern rule (% matches any)   │
│ $@           →  Target name (the .pdf file)    │
│ $<           →  First prerequisite (.py file)  │
│ @cmd         →  Run cmd silently (no echo)     │
│ \            →  Line continuation              │
└────────────────────────────────────────────────┘
```


By the way, in the above, what happens if `~/tmp` does not exist?

Your job: build tools that save future-you time.

**grep took one hour. Your tools can too.**

---

## Part 2: Shell Basics (bash.rc)

### What is bash.rc?

It runs every time you open a terminal. Think of it as your personal
config.

```sh
# Load it
source bash.rc

# Or make it executable
chmod +x bash.rc
./bash.rc
```

### Shell as Glue

Shell sucks at computation:
```sh
# This is painful
result=$((1234 * 5678))
```

Shell excels at delegation:
```sh
# This is beautiful
python3 -c "print(1234 * 5678)"
awk 'BEGIN {print 1234 * 5678}'
bc <<< "1234 * 5678"
```

Pick the right tool. Use shell to connect them.

### Functions > Aliases

```sh
# Alias (simple text swap)
alias ll='ls -la'

# Function (logic allowed)
c() { cd "$1"; ls; }
```

```
┌─ TRY THIS ────────────────────────────────────┐
│ 1. Add this to your terminal:                 │
│    c() { cd "$1"; ls; }                       │
│                                               │
│ 2. Try: c /tmp                                │
│                                               │
│ 3. What happened? Why is this better than:   │
│    alias c='cd /tmp; ls'                      │
└───────────────────────────────────────────────┘
```

### Example: Color Your Life

```sh
# From bash.rc
red() { tput setaf 1; }
gre() { tput setaf 2; }
blu() { tput setaf 4; }
clr() { tput sgr0; }
```

Use it:
```sh
echo "$(red)ERROR$(clr): failed"
echo "$(gre)OK$(clr): passed"
```

What Just Happened?
-------------------
1. tput setaf 1 outputs escape codes for red text
2. $(red) captures those codes and inserts them
3. Your text becomes red
4. $(clr) resets color to normal

### Example: The `hi` Utility

Highlight columns in text. Shell calls awk to do the work:

```sh
# Syntax: hi <column_number> [color]
cat data.csv | hi 1 2    # highlight columns 1 and 2

# How it works (shell glues, awk computes)
hi() {
  gawk -v cols="$*" '
    BEGIN { split(cols, c) }
    { for(i in c) $(c[i]) = "\033[32m" $(c[i]) "\033[0m"; print }
  '
}
```

```
┌─ Reading Guide ────────────────────────────────┐
│ gawk -v cols="$*"  →  Pass shell var to awk    │
│ "$*"               →  All arguments as string  │
│ $(c[i])            →  Access awk array         │
│ \033[32m           →  ANSI color code (green)  │
└────────────────────────────────────────────────┘
```

Try:
```sh
echo "name age city" | hi 2
```

### Building Your Own Tool Ecosystem

Your `bash.rc` extends Unix. Add functions to `PATH`:

```sh
# In bash.rc
export PATH="$HOME/bin:$PATH" # my code overrides system code

# Create ~/bin/mycmd
cat > ~/bin/mycmd << 'EOF'
#!/bin/bash
echo "My custom command!"
EOF
chmod +x ~/bin/mycmd

# Now anyone (including you) can call it
mycmd
```

You just joined the Unix community. Your tool is now discoverable.

By the way, the above is an example of a "here document".

### Here Documents

Feed multi-line text to commands without temp files:

```bash
# Basic: redirect to command
cat > file.txt << EOF
line 1
line 2
EOF

# Pipe to processing
cat << EOF | grep "error"
info: starting
error: failed
info: done
EOF

# Quote EOF to disable variable expansion
cat << 'EOF' | wc -l
$HOME won't expand
$(date) won't execute
EOF

# Indent with <<- (strips leading tabs, not spaces)
if true; then
	cat <<- END
	indented text
	stays readable
	END
fi
```

```
┌─ Reading Guide ────────────────────────────────┐
│ << EOF       →  Read until line with just EOF  │
│ << 'EOF'     →  Same but no variable expansion │
│ <<- EOF      →  Strip leading tabs             │
└────────────────────────────────────────────────┘
```

Quick and dirty macro system:

```gawk
src() { cat<<-'EOF' | sed 's/wme/n,mu,m2,sd,has,rows,nump,names/g'

BEGIN { K=1
        M=2
        main("header"); rogues() }

function main(go,     wme,nn,acc) {
  while(getline>0) {
    gsub(/[ \t]*/,"")
    acc += @go($NF, ++nn, wme)
    go = "data" }
  return acc/(nn - 20) }

function header(_,__,     wme,i) {
 for(i=1;i<=NF;i++) {
   names[$i]
   if (i ~ /^[A-Z]/) nump[i] }}

function data(k,nn,     wme,i,out) {
  if (nn > 20) out = k == likes(wme,nn,length(n))
  train(k,wme)
  return out }

function train(k, wme,i) {
  n[k]++
  r = length(r
  for(i=1;i<NF;i++) {
    x = $i+0
    x = x==$i ? x : $i
    if ($i != "?") 
      i in nump ? num(k,i,$i,wme) : sym(k,i,$i,wme)}

... 200 lines deleted ...
EOF
}

[[ -t 0 ]] && gawk -f <(src) "$@" || gawk -f <(src)
```

What Just Happened?
-------------------
1. src() function prints AWK code with placeholder "wme"
2. sed replaces "wme" with actual field names
3. gawk runs the generated code
4. `[[ -t 0 ]]` - Test if stdin (file descriptor 0) is a terminal
5. `&& gawk -f <(src) "$@"` - If true (terminal), process files from arguments
6. `|| gawk -f <(src)` - If false (pipe), process from stdin
7. Result: template expansion without a preprocessor

Usage examples:
```sh
./script.sh file.csv          # Uses first gawk (reads file)
cat data.csv | ./script.sh    # Uses second gawk (reads stdin)
```

Not so dirty version of the above (uses a very complicated regular expression... not for the meek).

```sh
#!/usr/bin/env bash
src() { cat <<'EOF'
BEGIN {
  a.i.j = 42
  print a.i.j
  a.i=223
  array(a.i)
  print .123 }

#--------------------------------------------------------------------
EOF
}

prep() { gawk '
  BEGIN { print "# add 2 blank lines to fix line numbers (in errors)\n"  } 
        { print gensub(/\.([a-zA-Z_][a-zA-Z0-9_]*)/, "[\"\\1\"]", "g")}'; }

[[ -t 0 ]] && gawk -f <(src | prep) "$@" || gawk -f <(src | prep)
```


### Git-Aware Prompt

```sh
# Show current branch
branch() { git rev-parse --abbrev-ref HEAD 2>/dev/null; }

# Show * if uncommitted changes
dirty() {
  git status --porcelain 2>/dev/null | grep -q . && echo "*"
}

# Build prompt
PS1='\w $(branch)$(dirty) > '
```

```
┌─ Reading Guide ────────────────────────────────┐
│ 2>/dev/null  →  Hide error messages            │
│ grep -q .    →  Quiet mode, just return 0/1    │
│ && echo "*"  →  Print * only if grep succeeded │
└────────────────────────────────────────────────┘
```

Result: `/home/tim main* >`

### Exit Codes: The Shell's Truth

```sh
# Success = 0
true
echo $?    # 0

# Failure = non-zero
false
echo $?    # 1

# Chain commands with exit codes
grep -q "TODO" file.txt && echo "Found" || echo "Missing"

# Your scripts return codes too
check() {
  grep -q "TODO" "$1" && return 1
  return 0
}

if check myfile.py; then
  echo "Clean!"
else
  echo "Has TODOs"
fi
```

Exit codes let programs talk to each other without knowing each other.

### Essential Shell Variables (Quick Reference)

```sh
$HOME      # Your home directory
$PATH      # Where shell finds commands
$PWD       # Current directory
$OLDPWD    # Previous directory (for cd -)
$USER      # Your username
$?         # Exit code of last command
$0         # Script name
$1 $2 $3   # Positional arguments
$@         # All arguments (preserves spacing)
$*         # All arguments (merged)
$#         # Number of arguments
$$         # Current process ID
```

Example:
```bash
# One-liner demo
echo "$0 ran as $USER from $PWD with $# args: $@. Last exit: $?"
```

---

## Part 2.5: Shell Wars - sh vs bash vs zsh

### The Family Tree

```sh
sh    # Original Bourne shell (1979)
bash  # Bourne Again SHell (1989) - sh + features
zsh   # Z Shell (1990) - bash + even more features
```

### Key Differences

```sh
# sh: minimal, POSIX-standard
if [ "$x" = "5" ]; then echo "yes"; fi

# bash: arrays, better strings, [[ ]]
if [[ $x == 5 ]]; then echo "yes"; fi
files=( *.txt )

# zsh: autocomplete, themes, oh-my-zsh
# Amazing for interactive use!
```

### For Scripts: Use Bash

**Google's Shell Style Guide:**
> "Bash is the only shell scripting language permitted for executables."

Why?
- Installed everywhere
- Feature-rich enough
- Consistent behavior
- No POSIX-compatibility headaches

```sh
#!/bin/bash
set -euo pipefail  # Fail fast, catch errors

# Now you can use bash features freely
[[ -f "$file" ]] && echo "exists"
```

```
┌─ Reading Guide ────────────────────────────────┐
│ set -e       →  Exit on any error              │
│ set -u       →  Exit on undefined variable     │
│ set -o pipe  →  Exit on pipe failure           │
│ set -euo...  →  All three safety flags         │
└────────────────────────────────────────────────┘
```

### For Interactive Use: zsh Wins

zsh gives you **bling**:
- Better tab completion
- Syntax highlighting as you type
- Themes via oh-my-zsh
- Smart history search

```sh
# In zsh
cd ~/pro<TAB>      # Shows: ~/projects/
git co ma<TAB>     # Shows: main master
```

**Recommendation:** zsh for daily terminal work, bash for scripts.

---

## Part 3: Makefile Basics

### What is Make?

A task runner. Define targets, run them by name.

```makefile
# Simplest possible
hello:
	echo "Hello world"
```

Run it:
```sh
make hello
```

┌─ CRITICAL ────────────────────────────────────┐
│ Makefiles use TABS, not spaces for indents.  │
│ If you get "missing separator", check tabs.  │
└───────────────────────────────────────────────┘

### Pattern: Target Depends on Files

```makefile
report.txt: data.csv
	wc -l < data.csv > report.txt
```

Logic: if `data.csv` is newer than `report.txt`, rebuild.

```
┌─ TRY THIS ────────────────────────────────────┐
│ 1. Create Makefile with above rule            │
│ 2. Create data.csv with some lines            │
│ 3. Run: make report.txt                       │
│ 4. Run it again. What message do you see?     │
│ 5. Touch data.csv. Run make again. Why?       │
└───────────────────────────────────────────────┘
```

### Pattern: Phony Targets

```makefile
.PHONY: clean
clean:
	rm -rf *.o *.pyc
```

Phony = doesn't create a file, always runs.

---

## Part 4: Make Quick Reference

Before diving into your Makefile, you need to read Make syntax.

### Automatic Variables

```makefile
target: prereq1 prereq2
	command uses these variables

$@    # Target name (the thing being built)
$<    # First prerequisite
$^    # All prerequisites
$*    # Stem of pattern match (the % part)
```

Example:
```makefile
%.pdf: %.py
	echo "Building $@ from $<"
	# $@ = something.pdf
	# $< = something.py
```

### Variable Assignment

```makefile
X := $(shell date)      # := immediate (evaluated once)
Y = $(shell date)       # =  lazy (evaluated each use)
Z ?= default            # ?= set only if not already set
```

```
┌─ TRY THIS ────────────────────────────────────┐
│ Create Makefile:                              │
│   A := $(shell date)                          │
│   B = $(shell date)                           │
│   test:                                       │
│       @echo "A: $(A)"                         │
│       @sleep 1                                │
│       @echo "A: $(A)"                         │
│       @echo "B: $(B)"                         │
│       @sleep 1                                │
│       @echo "B: $(B)"                         │
│                                               │
│ Run: make test                                │
│ What's different? Why?                        │
└───────────────────────────────────────────────┘
```

### Pattern Rules

```makefile
%.o: %.c
	gcc -c $< -o $@

# Matches any .c → .o conversion
# make foo.o finds foo.c and runs: gcc -c foo.c -o foo.o
```

---

## Part 5: Deep Dive - YOUR Makefile

Let's dissect the real thing.

### Variables: Self-Awareness

```makefile
GIT_ROOT := $(shell git rev-parse --show-toplevel)
```

Why? So `make clean` works from any subdirectory.

```makefile
clean:
	cd $(GIT_ROOT) && rm -rf build/
```

### Colors

```makefile
R := $(shell tput setaf 1)
G := $(shell tput setaf 2)
B := $(shell tput setaf 4)
X := $(shell tput sgr0)
```

Use them:
```makefile
test:
	@echo "$(G)PASS$(X): all tests ok"
```

```
┌─ Reading Guide ────────────────────────────────┐
│ $(shell cmd) →  Run shell command at parse    │
│ tput setaf N →  Set foreground color N        │
│ tput sgr0    →  Reset all attributes          │
│ @echo        →  Echo without showing command  │
└────────────────────────────────────────────────┘
```

### `make help`

Self-documenting via inline comments.

```makefile
.PHONY: help
help:  ## Show this help
	@gawk 'BEGIN {FS = ":.*?## "} \
	       /^[a-zA-Z_-]+:.*?## / \
	       {printf "$(B)%-10s$(X) %s\n", $$1, $$2}' \
	       $(MAKEFILE_LIST)
```

```
┌─ Reading Guide ────────────────────────────────┐
│ FS = ":.*?## "    →  Field separator (regex)   │
│ /pattern/         →  Match lines               │
│ $$1 $$2           →  $$ escapes $ for shell    │
│ $(MAKEFILE_LIST)  →  Current Makefile name     │
└────────────────────────────────────────────────┘
```

How it works:
1. Read the Makefile itself (`$(MAKEFILE_LIST)`)
2. Find lines matching `target: ## comment`
3. Print `target` in blue, `comment` in white

Try it:
```sh
make help
```

Output:
```
help       Show this help
install    Install dependencies
test       Run tests
```

### `make sh`

Drop into your custom shell.

```makefile
sh:  ## Start shell with bash.rc loaded
	@bash --rcfile bash.rc -i
```

Why `@`? Suppress echoing the command.

Try:
```sh
make sh
# Now you're in a shell with all your custom functions
```

### `make install`

Set up your environment.

```makefile
install:  ## Link bash.rc to ~/.bashrc
	@echo "source $(PWD)/bash.rc" >> ~/.bashrc
	@echo "$(G)Installed!$(X) Restart terminal."
```

One-time setup. Now `bash.rc` loads automatically.

### `make ok`

Run all checks before committing.

```makefile
ok:  ## Run lint + tests
	@$(MAKE) lint
	@$(MAKE) test
	@echo "$(G)Ready to commit$(X)"
```

```
┌─ Reading Guide ────────────────────────────────┐
│ $(MAKE)      →  Recursive make (not "make")    │
│ @$(MAKE) foo →  Call another target silently   │
└────────────────────────────────────────────────┘
```

Pattern: orchestrate other targets.

### `make push`

Safe push with checks.

```makefile
push:  ## Run ok, then git push
	@$(MAKE) ok
	git push origin $(shell git branch --show-current)
```

Never push broken code again.

### `make clean`

Remove generated files.

```makefile
clean:  ## Remove build artifacts
	@cd $(GIT_ROOT) && rm -rf \
	  build/ dist/ *.egg-info \
	  **/__pycache__ **/*.pyc
```

Pattern: `rm -rf` is safe because we `cd $(GIT_ROOT)` first.

### `make py` → PDF

Bundle complex commands.

```makefile
%.pdf: %.py  ## Convert Python to PDF docs
	@echo "$(B)Building PDF$(X) for $<"
	python3 -m pydoc -w $< && \
	  mv $*.html $*.pdf
	@echo "$(G)Created$(X) $@"
```

Pattern rule: `%` matches anything.

```sh
make script.pdf    # Converts script.py → script.pdf
```

Why this matters: Instead of typing:
```sh
python3 -m pydoc -w script && mv script.html script.pdf
```

You type:
```sh
make script.pdf
```

Shell glues Python + mv. Make glues shell commands.

---

## Part 6: Common Errors and Debugging

### When Something Breaks

```
┌─ DEBUG STRATEGY ──────────────────────────────┐
│ 1. Run with debugging:                        │
│    bash -x script.sh    # Shows each command  │
│    make -n target       # Dry-run (no exec)   │
│                                               │
│ 2. Add echo statements:                       │
│    echo "DEBUG: var=$var"                     │
│                                               │
│ 3. Check exit codes:                          │
│    command                                    │
│    echo $?              # 0=ok, else fail     │
│                                               │
│ 4. Simplify until it works:                   │
│    Comment out half, does it work now?        │
│    Binary search the problem                  │
└───────────────────────────────────────────────┘
```

### Common Error Messages

```
make: *** No rule to make target 'foo'
  → You typed "make foo" but Makefile has no "foo:" target

make: *** missing separator. Stop.
  → You used spaces instead of TABS for indentation

bash: syntax error near unexpected token ')'
  → Mismatched quotes or parentheses. Check line above error

command not found
  → Program isn't in PATH. Use "which <cmd>" to check

.bashrc: line 12: `$1': not a valid identifier
  → Can't use $1 outside a function. Wrap in function() { ... }

permission denied
  → Need chmod +x script.sh to make it executable
```

---

## Part 7: One-Page Reference Card

```
┌─────────────────────────────────────────────────────────────────────┐
│ SHELL CHEAT SHEET                                                   │
├─────────────────────────────────────────────────────────────────────┤
│ VARIABLES                                                           │
│   name="value"         Assign (no spaces around =)                  │
│   $name                Use variable                                 │
│   "$name"              Use with quotes (preserves spaces)           │
│   $(command)           Capture command output                       │
│                                                                     │
│ REDIRECTION                                                         │
│   cmd > file           Overwrite file                               │
│   cmd >> file          Append to file                               │
│   cmd 2> file          Errors to file                               │
│   cmd1 | cmd2          Pipe output                                  │
│                                                                     │
│ TESTS                                                               │
│   [[ -f file ]]        File exists?                                 │
│   [[ -d dir ]]         Directory exists?                            │
│   [[ -z "$x" ]]        String empty?                                │
│   [[ "$a" == "$b" ]]   Strings equal?                               │
│                                                                     │
│ CONTROL                                                             │
│   cmd1 && cmd2         Run cmd2 if cmd1 succeeds                    │
│   cmd1 || cmd2         Run cmd2 if cmd1 fails                       │
│   if [[ test ]]; then ... fi                                        │
│   for x in *; do ... done                                           │
│                                                                     │
│ SPECIAL VARIABLES                                                   │
│   $0                   Script name                                  │
│   $1 $2 $3             Arguments                                    │
│   $@                   All arguments                                │
│   $#                   Argument count                               │
│   $?                   Last exit code                               │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│ MAKE CHEAT SHEET                                                    │
├─────────────────────────────────────────────────────────────────────┤
│ SYNTAX                                                              │
│   target: prereqs      Build target from prereqs                    │
│   <TAB>command         Commands MUST use tabs                       │
│   .PHONY: target       Always run (no file check)                   │
│                                                                     │
│ VARIABLES                                                           │
│   X := value           Immediate assignment                         │
│   Y = value            Lazy assignment                              │
│   Z ?= value           Default value                                │
│   $(X)                 Use variable                                 │
│   $(shell cmd)         Run shell command                            │
│                                                                     │
│ AUTOMATIC VARIABLES                                                 │
│   $@                   Target name                                  │
│   $<                   First prerequisite                           │
│   $^                   All prerequisites                            │
│   $*                   Stem in pattern                              │
│                                                                     │
│ PATTERNS                                                            │
│   %.o: %.c             Pattern rule (% = wildcard)                  │
│   @command             Silent (no echo)                             │
│   $(MAKE) target       Recursive make                               │
└─────────────────────────────────────────────────────────────────────┘
```
