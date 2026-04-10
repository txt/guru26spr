# One-Week Homework: Smalltalk from Zero to Tiny DSL

This homework is for complete beginners. It uses **GNU Smalltalk** as a
command-line, text-file-first Smalltalk system. GNU Smalltalk runs as
`gst [flags] [file ...]`; if you pass one or more files, it reads and executes
them in order, then exits. ([GNU][1])

The goal is to learn three things:

1. basic message sending
2. collection processing with blocks
3. a tiny domain-specific API that captures a repeated idiom

Keep it simple. One week. Small programs. Plain text files.

---

## What to install

Use **GNU Smalltalk**.

A source tarball is available from the GNU FTP archive as
`smalltalk-3.2.5`. ([ftp.gnu.org][2])

If you are on macOS with Homebrew, Homebrew currently lists a
`gnu-smalltalk` formula (version `3.2.5`). ([Homebrew Formulae][3])

### Suggested install paths

#### macOS with Homebrew

```bash
brew install gnu-smalltalk
gst --version
```

Homebrew lists `gnu-smalltalk` as an available formula. ([Homebrew Formulae][3])

#### Build from source

```bash
curl -O https://ftp.gnu.org/gnu/smalltalk/smalltalk-3.2.5.tar.gz
tar xzf smalltalk-3.2.5.tar.gz
cd smalltalk-3.2.5
./configure
make
sudo make install
gst --version
```

The GNU FTP directory includes the `smalltalk-3.2.5.tar.gz` source archive.
([ftp.gnu.org][2])

---

## How you will run code

Create plain text files ending in `.st`, then run them from the shell.

```bash
gst hello.st
gst part1.st
gst part2.st
```

GNU Smalltalk executes files you pass on the command line and exits when it
reaches end-of-file. ([GNU][1])

---

## Submission

Submit a folder containing:

* `hello.st`
* `collections.st`
* `miniDsl.st`
* `README.md`

Your `README.md` should include:

* your name
* how to run each file
* one paragraph on what felt easy
* one paragraph on what felt odd or surprising

---

## Learning targets

By the end of the week, you should be able to:

* send messages to numbers, strings, and collections
* use blocks with collection methods
* print results clearly
* spot repeated domain patterns in prose
* turn one repeated pattern into a tiny DSL-like message

---

## Part A: Hello, messages, and printing

Make a file called `hello.st`.

### Task A1

Write code that prints:

* your name
* the result of `3 + 4`
* the size of the string `'hello'`

A simple output pattern is:

```smalltalk
'Hello world' printNl.
```

### Task A2

Store values in variables and print them.

Use:

* a number
* a string
* an array literal like `#(1 2 3 4)`

Print at least three lines.

### Minimum success check

When I run:

```bash
gst hello.st
```

I should see at least 5 readable output lines.

---

## Part B: Collections and blocks

Make a file called `collections.st`.

This is the main technical part.

Use one collection throughout, for example:

```smalltalk
nums := #(1 2 3 4 5 6).
```

### Task B1: `do:`

Print every item in the collection, one per line.

Example shape:

```smalltalk
nums do: [ :each | each printNl ].
```

### Task B2: `collect:`

Create a new collection containing doubled values.

Print the result.

Example idea:

* input: `#(1 2 3 4)`
* output: something like `#(2 4 6 8)`

### Task B3: `select:`

Keep only the even numbers.

Print the result.

### Task B4: `reject:`

Reject numbers less than 4.

Print the result.

### Task B5: `inject:into:`

Compute a sum using accumulation.

For example, sum all numbers in `nums`.

This is the "fold" / "reduce" pattern.

### Minimum success check

Your program should clearly print:

* the original collection
* the result of `collect:`
* the result of `select:`
* the result of `reject:`
* the result of `inject:into:`

### Hint

A nice pattern is to label output:

```smalltalk
'original:' printNl.
nums printNl.
```

---

## Part C: One tiny DSL move

Make a file called `miniDsl.st`.

This part is intentionally gentle. You are **not** building a full parser.
You are spotting a repeated idiom and giving it a better name.

### Step C1: Read this user text

Use this paragraph as your source text:

> In our grading workflow, we first keep only passing scores. Then we drop
> any score above 100 as suspicious input. Then we compute the total of what
> remains. We do this same three-step cleanup over and over in several tools.

### Step C2: Extract the common idiom

Write 3-5 lines in comments at the top of your file saying what the repeated
pattern is.

For example, something like:

* filter valid items
* reject bad items
* reduce to one answer

Do not overthink this. Just name the repetition.

### Step C3: Code the idiom in a friendly way

Define a tiny helper method or object so the user code reads more like an
intent than a mechanism.

Your beginner goal is something like this:

```smalltalk
cleanedTotal := ScoreTools totalOfCleanScores: scores.
```

or, if you want to be a little fancier:

```smalltalk
cleanedTotal := scores cleanAndTotal.
```

Either is fine.

### What the helper should do

Given a collection of numbers, it should:

1. keep only scores `>= 50`
2. reject scores `> 100`
3. add the remaining scores

### Input to test with

Use:

```smalltalk
scores := #(20 55 70 101 85 49 100 200).
```

### Expected reasoning

* passing scores are `55 70 101 85 100 200`
* reject `101` and `200`
* total should be `55 + 70 + 85 + 100 = 310`

So your program should print `310`.

---

## Constraints on difficulty

Keep the DSL part tiny.

You are **not** required to:

* define a full grammar
* parse English
* subclass complicated framework classes
* do metaprogramming

You **are** required to:

* notice a repeated expert habit
* wrap that habit in one clearer message
* make the final use-site read better than raw steps

That is enough for an intro.

---

## Suggested structure for `miniDsl.st`

Here is a safe beginner shape:

1. define a helper class or class-side method
2. give it one clearly named operation
3. call it on sample data
4. print the result

The key idea is:

* raw code shows the mechanism
* your tiny DSL name shows the intent

---

## Optional extra credit

If you finish early, do one of these:

* add a second helper like `cleanScores:`
* write a second example paragraph and extract a second idiom
* compare "raw steps" vs "tiny DSL" in 4-6 lines of prose

---

## A tiny example of the mindset

The raw version might look like:

* select passing
* reject impossible
* inject into a total

The DSL version gives that shape a name:

* `totalOfCleanScores:`

That is the lesson.

You are not trying to impress anyone with power.
You are learning how OO can absorb a repeated control pattern and turn it into
a domain phrase.

[1]: https://www.gnu.org/software/smalltalk/manual/gst.html?utm_source=chatgpt.com "GNU Smalltalk User's Guide"
[2]: https://ftp.gnu.org/gnu/smalltalk/?C=N%3BO%3DD&utm_source=chatgpt.com "Index of /gnu/smalltalk"
[3]: https://formulae.brew.sh/formula/?utm_source=chatgpt.com "homebrew-core"

