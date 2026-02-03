.

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

Note: Thompson di not "ship" grep to MaMahon. He just added it to his "bin".
Now anyone on the same file system can access grep bu adding Ken's path to their startup:

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

### Why This Matters

**grep exists because Unix decentralized tool creation.**

Everyone can add to their own `/usr/myNamebin`. Shell finds it. Community grows.

No permission needed. No central registry. Just:
1. Write a program
2. Put it in `PATH`
3. Everyone can use it

This lecture: you're joining that tradition.

### Your Turn

Build your own tools. Make them small. Ship them.
Let reality tell you what's needed next.

---

## Part 1: Why Bother?

Typing is expensive. Remembering is expensive. Let's automate.

```sh
# Bad: type this 50 times
python3 -m pydoc -w myfile && mv myfile.html myfile.pdf

# Good: type this once
make pdf
```

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

Try it:
```sh
c /tmp          # cd + ls in one command
```

### Example: Color Your Life

```sh
# From bash.rc
red() { tput setaf 1; }
gre() { tput setaf 2; }
```

Use it:
```sh
echo "$(red)ERROR$(tput sgr0): failed"
echo "$(gre)OK$(tput sgr0): passed"
```

### Example: The `hi` Utility

Highlight columns in text. Shell calls awk to do the work:

```sh
# Syntax: hi <column_number> [color]
cat data.csv | hi 1 2    # highlight column 1 in green

# How it works (shell glues, awk computes)
hi() {
  gawk -v cols="$*" '
    BEGIN { split(cols, c) }
    { for(i in c) $(c[i]) = "\033[32m" $(c[i]) "\033[0m"; print }
  '
}
```

Try:
```sh
echo "name age city" | hi 2
```

### Building Your Own Tool Ecosystem

Your `bash.rc` extends Unix. Add functions to `PATH`:

```sh
# In bash.rc
export PATH="$HOME/bin:$PATH" # my code overrides system code.

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

BY the way, the above is an example of a "here doc"

```markdown
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


### Essential Shell Variables
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

Example1:

```bash
# One-liner demo
echo "$0 ran as $USER from $PWD with $# args: $@. Last exit: $?"
```

Example2:

```bash
# Tiny example using many shell variables
backup() {
  cp "$1" "$HOME/backups/$USER-$(basename $1)-$$.bak" && 
  echo "$0: Saved $# file(s). Exit: $?" || 
  cd "$OLDPWD"
}
```

 
## Part X: Shell Wars - sh vs bash vs zsh

### The Family Tree

```sh
sh    # Original Bourne shell (1979)
bash  # Bourne Again SHell (1989) - sh + features
zsh   # Z Shell (1990) - bash + even more features
...   # etc
...   # etc
```

zsh, best for bling. see ["oh my zsh"](https://github.com/ohmyzsh):

<img width="2170" height="2418" alt="image" src="https://github.com/user-attachments/assets/3db4ba6a-ea1d-4d04-b6c5-27813774fd64" />

### Key Differences

```sh
# sh: minimal, POSIX-standard
if [ "$x" = "5" ]; then echo "yes"; fi

# bash: arrays, better strings, [[  ]]
if [[ $x == 5 ]]; then echo "yes"; fi
files=( *.txt )

# zsh: autocomplete, themes, oh-my-zsh
# Amazing for interactive use!
 

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

### The Future: Collaborative Shells

New shells rethinking the command line:

**Jupyter notebooks for shell:**
- Commands + output persist
- Shareable, reproducible
- Mix shell + Python + SQL

What notebooks should be:
- Version controlled
- Text-based (not JSON blobs)
- Composable pipelines

Tools emerging:
- `nushell` - structured data pipelines
- `xonsh` - Python + shell hybrid
- Notebook tools for shell workflows

The command line is evolving from solo work to team collaboration.

 

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

### Pattern: Target Depends on Files

```makefile
report.txt: data.csv
	wc -l < data.csv > report.txt
```

Logic: if `data.csv` is newer than `report.txt`, rebuild.

### Pattern: Phony Targets

```makefile
.PHONY: clean
clean:
	rm -rf *.o *.pyc
```

Phony = doesn't create a file, always runs.

---

## Part 4: Deep Dive - YOUR Makefile

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

### `make lint`

Check code quality.

```makefile
lint:  ## Run style checks
	@find . -name "*.py" | xargs pylint --score=n
```

Pattern: `find | xargs` for batch processing.

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

## Part 5: Advanced Patterns

### Parallel Execution

```makefile
test-all:
	@find tests/ -name "test_*.py" | \
	  xargs -P 4 -I {} python3 {}
```

`-P 4` = run 4 tests in parallel.

### Conditional Logic

```makefile
deploy:
ifeq ($(shell git status --porcelain),)
	@echo "Deploying..."
else
	@echo "$(R)ERROR$(X): uncommitted changes"
	@exit 1
endif
```

### Variables from Environment

```makefile
VERSION ?= 1.0.0

release:
	@echo "Releasing v$(VERSION)"
```

Usage:
```sh
make release              # Uses VERSION=1.0.0
VERSION=2.0.0 make release  # Override
```

---

## Homework (1 Week): CSV Processor

**Your Lee McMahon moment**: Build tools for CSV analysis.

Ship something tiny. Let your classmates use it. Iterate.

### Requirements (All Students)

Create two files:

#### `csv.rc`

```sh
#!/bin/bash

# Count rows and columns (shell glues tail + wc + tr)
count() {
  local rows=$(tail -n +2 "$1" | wc -l)
  local cols=$(head -1 "$1" | tr ',' '\n' | wc -l)
  echo "Rows: $rows, Cols: $cols"
}

# Summarize numeric column (shell glues, awk computes)
summarize() {
  local file=$1
  local col=$2
  gawk -F, -v c=$col '
    NR>1 { sum+=$c; n++ }
    END { printf "Mean: %.2f, Sum: %.2f\n", sum/n, sum }
  ' "$file"
}

# Show specific columns (shell glues cut + column)
showcol() {
  local file=$1
  shift
  cut -d, -f"$*" "$file" | column -t -s,
}
```

#### `Makefile`

```makefile
B := $(shell tput setaf 4)
X := $(shell tput sgr0)

.PHONY: help
help:  ## Show this help
	@gawk 'BEGIN {FS = ":.*?## "} \
	       /^[a-zA-Z_-]+:.*?## / \
	       {printf "$(B)%-12s$(X) %s\n", $$1, $$2}' \
	       $(MAKEFILE_LIST)

setup:  ## Create data/ directory
	@mkdir -p data reports

view:  ## Display CSV nicely
	@column -t -s, data/*.csv

report:  ## Generate summary for all CSVs
	@for f in data/*.csv; do \
	  echo "=== $$f ===" > reports/$$(basename $$f .csv).txt; \
	  bash csv.rc count "$$f" >> reports/$$(basename $$f .csv).txt; \
	  bash csv.rc summarize "$$f" 2 >> reports/$$(basename $$f .csv).txt; \
	done

clean:  ## Remove reports
	@rm -rf reports/*.txt
```

### Test It

```sh
# Create sample data
cat > data/sales.csv << EOF
month,revenue,costs
Jan,1000,600
Feb,1500,700
Mar,1200,650
EOF

# Run commands
make setup
make view
make report
cat reports/sales.txt
```

Expected output in `reports/sales.txt`:
```
=== data/sales.csv ===
Rows: 3, Cols: 3
Mean: 1233.33, Sum: 3700.00
```

### Deliverables

1. `csv.rc` with `count()`, `summarize()`, `showcol()`
2. `Makefile` with working `help` target
3. `README.md` showing `make help` output
4. Sample `data/*.csv` and generated `reports/*.txt`

**Ship it to a classmate. Get feedback. Iterate.**

---

### Graduate Extension (+40%)

Add these to your submission:

#### 1. Parallel Processing

```makefile
report-parallel:  ## Generate reports in parallel
	@ls data/*.csv | xargs -P 4 -I {} bash -c \
	  'f={}; o=reports/$$(basename $$f .csv).txt; \
	   echo "=== $$f ===" > $$o; \
	   bash csv.rc count "$$f" >> $$o'
```

#### 2. Validation

```makefile
validate:  ## Check CSV format
	@for f in data/*.csv; do \
	  awk -F, 'NR==1 {n=NF} NF!=n {print "Bad: " FILENAME; exit 1}' $$f; \
	done && echo "All CSVs valid"
```

#### 3. Dynamic Column Selection

Modify `summarize()` to accept column name, not just number:

```sh
summarize() {
  local file=$1
  local colname=$2
  gawk -F, -v col="$colname" '
    NR==1 { for(i=1;i<=NF;i++) if($i==col) c=i }
    NR>1 { sum+=$c; n++ }
    END { printf "Mean: %.2f, Sum: %.2f\n", sum/n, sum }
  ' "$file"
}
```

Usage:
```sh
summarize data/sales.csv revenue
```

#### 4. Auto-Generated Help in csv.rc

```sh
# In csv.rc
help() {
  gawk '/^[a-z_]+\(\)/ {print $1}' csv.rc | sed 's/().*//'
}
```

#### 5. Multi-Language Pipeline

Demonstrate shell as glue:

```makefile
analyze:  ## Run multi-language analysis
	@echo "$(B)Step 1:$(X) Extract with Python"
	@python3 -c "import csv; \
	  print(list(csv.reader(open('data/sales.csv'))))"
	@echo "$(B)Step 2:$(X) Compute with AWK"
	@awk -F, 'NR>1 {sum+=$$2} END {print "Total:", sum}' \
	  data/sales.csv
	@echo "$(B)Step 3:$(X) Format with Ruby"
	@ruby -rcsv -e 'CSV.foreach(ARGV[0]) {|r| puts r.join(" | ")}' \
	  data/sales.csv
```

---

## Grading Rubric

| Item                          | Points |
|-------------------------------|--------|
| `make help` works             | 20     |
| `csv.rc` functions work       | 30     |
| Reports generated correctly   | 30     |
| Code is clean, documented     | 20     |
| **Grad Extension (optional)** | +40    |

Submit: `<lastname>_csv.zip` containing all files.

---

## Key Takeaways

1. **Shell = glue, not compute**
2. **Make = orchestration, not execution**
3. **Decentralized tools** > monolithic systems
4. **Exit codes** > exceptions in shell
5. **Small tools, fast iteration** > big plans

**Like grep: small tools, real users, quick iterations.**

Questions? Read the source. It's only 50 lines.
```
