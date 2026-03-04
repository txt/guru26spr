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


# Smalltalk Mini-Tutorial

In Smalltalk, we do not start by writing functions.
We start by sending messages.

Everything is an object.

That includes:

* numbers
* strings
* collections
* classes
* blocks
* even control structures are mostly message sends

This makes Smalltalk a very clean language for building little languages.

You do not just write code *in* the language.
You can reshape the language by defining new messages and new objects.

That is why Smalltalk is a natural place to build a DSL.

Basic conventions:

* names starting with uppercase are usually classes: `Point`, `Array`
* names starting with lowercase are variables: `x`, `total`
* messages come in three styles:

  * unary: `x size`
  * binary: `3 + 4`
  * keyword: `array at: 3 put: 99`

---

## 1. Everything is a message send

Smalltalk code is built from message sends.

```smalltalk
3 + 4
```

This means:

* send the message `+ 4`
* to the object `3`

So even arithmetic is object-oriented.

Strings too:

```smalltalk
'hello' size
```

This sends `size` to the string `'hello'`.

Collections:

```smalltalk
#(1 2 3) first
```

This sends `first` to an array literal.

The big idea is simple:

* objects receive messages
* methods decide how to respond

---

## 2. The three kinds of messages

Smalltalk has three kinds of messages.

### Unary messages

No arguments:

```smalltalk
x class
x printString
```

### Binary messages

Usually symbolic, one argument:

```smalltalk
3 + 4
10 > 7
```

### Keyword messages

Named arguments:

```smalltalk
array at: 2
array at: 2 put: 99
```

Keyword messages are one of Smalltalk's nicest features.
They make code read like little sentences.

---

## 3. Variables and assignment

Assignment uses `:=`.

```smalltalk
x := 10.
y := x + 5.
```

A period ends a statement.

So this:

```smalltalk
x := 10.
y := x + 5.
y
```

returns `15`.

Smalltalk style is often a sequence of expressions, each sending messages.

---

## 4. Blocks: delayed computation

A block is code inside square brackets.

```smalltalk
[ 3 + 4 ]
```

This does not run yet.
It is an object representing deferred work.

To run it, send `value`.

```smalltalk
[ 3 + 4 ] value
```

That returns `7`.

Blocks may take arguments:

```smalltalk
[ :x | x + 1 ] value: 4
```

That returns `5`.

Blocks are central to Smalltalk because they let objects control *when* and
*how* other code runs.

This is the key to inversion of control.

---

## 5. Collections and iteration

Collections use blocks for control structures.

```smalltalk
#(1 2 3 4) do: [ :each | Transcript show: each printString ]
```

This means:

* send `do:` to the collection
* give it a block
* the collection decides how to iterate

Or collect results:

```smalltalk
#(1 2 3 4) collect: [ :x | x * 2 ]
```

That returns a new collection with doubled values.

Or filter:

```smalltalk
#(1 2 3 4) select: [ :x | x even ]
```

This style matters because the *collection* owns the loop.

You do not write loop mechanics yourself.
You provide behavior, and the object applies it.

That is inversion of control in everyday form.

---

## 6. Control flow is also messages

Conditionals are message sends to booleans.

```smalltalk
x > 0
  ifTrue: [ 'positive' ]
  ifFalse: [ 'not positive' ]
```

Loops are often block messages:

```smalltalk
[ x < 10 ] whileTrue: [
  x := x + 1
]
```

So in Smalltalk:

* booleans decide conditionals
* blocks decide repeated work
* objects own the control structure

This is very different from languages where `if` and `while` are fixed syntax.

In Smalltalk, much of control flow is open to extension.

---

## 7. Defining a class

A class packages state and behavior.

A simple example:

```smalltalk
Object subclass: #Counter
  instanceVariableNames: 'n'
  classVariableNames: ''
  poolDictionaries: ''
  category: 'Tutorial'
```

Add methods:

```smalltalk
Counter >> initialize
  n := 0

Counter >> inc
  n := n + 1

Counter >> value
  ^ n
```

Use it:

```smalltalk
c := Counter new.
c initialize.
c inc.
c inc.
c value
```

This returns `2`.

So objects are little bundles of data plus message handlers.

---

## 8. Why OO inversion of control matters

The big advantage of object-oriented inversion of control is this:

> put the variation where it belongs

Examples:

* collections own traversal
* booleans own branching
* streams own reading strategy
* UI widgets own event dispatch
* domain objects can own domain idioms

This gives real benefits:

* less repeated boilerplate
* common patterns become reusable messages
* extensions fit domain vocabulary
* users of the code write less mechanism, more intent

Instead of saying:

* first do this
* then branch here
* then loop there

you often say:

* here is the behavior
* object, you decide when to apply it

That is a deep advantage, not just syntactic sugar.

---

## 9. From OO to DSL

A DSL is a small language for a specific domain.

In Smalltalk, DSLs often emerge by:

* defining domain classes
* giving them domain-specific messages
* using blocks to capture user-supplied actions
* letting objects control sequencing

So instead of writing generic code, users write domain sentences.

For example, suppose the expert domain has rules.

A rough generic style might be:

```smalltalk
rule := Rule new.
rule condition: [ :ctx | ctx temperature > 100 ].
rule action: [ :ctx | ctx alarmOn ].
engine add: rule.
```

That already reads like a little language.

But we can go further.

---

## 10. A tiny DSL flavor

Suppose we want expert users to write:

```smalltalk
engine
  when: [ :ctx | ctx temperature > 100 ]
  then: [ :ctx | ctx alarmOn ].
```

This is just a keyword message protocol.

A possible sketch:

```smalltalk
Engine >> when: aBlock then: anotherBlock
  self addRule: (Rule
    condition: aBlock
    action: anotherBlock)
```

Now the domain idiom is captured in the message shape.

This is the Smalltalk DSL trick:

* use keyword messages to make readable phrases
* use blocks to package deferred behavior
* use objects to own the control

The "language" is not a parser hack.
It is ordinary OO design done well.

---

## 11. Specialized control structures

Now for your main goal: specialized control structures.

Suppose experts often say:

* try rules until one matches
* do the first applicable action
* run setup/cleanup around a task
* process records under a policy

In a conventional language, users may rewrite this pattern over and over.

In Smalltalk, you can capture it once.

For example:

```smalltalk
policy firstMatchDo: [ :rule | rule applyTo: ctx ].
```

Or:

```smalltalk
task
  withLoggingDo: [ :t | t run ].
```

Or:

```smalltalk
records under: securityPolicy do: [ :r | r process ].
```

These are domain-shaped control structures.

They work because:

* blocks capture the user action
* the receiving object controls timing, order, guards, retries, cleanup

That is inversion of control used to encode expert idioms.

---

## 12. A simple pattern for building a DSL

A beginner-friendly path is:

1. make plain domain objects
   `Rule`, `Engine`, `Policy`, `Task`

2. identify repeated expert idioms
   "first matching rule", "under policy", "retry until valid"

3. turn each idiom into a message
   `when:then:`, `under:do:`, `retryUntil:`

4. use blocks for custom behavior
   this keeps the extension point flexible

5. let the receiver own the mechanics
   the user writes intent, the object runs the pattern

That is the core recipe.

---

## 13. A good tutorial sequence from zero to DSL

A natural teaching order is:

1. everything is an object
2. message sends
3. assignment and expressions
4. blocks
5. collections with `do:`, `collect:`, `select:`
6. conditionals and loops as messages
7. defining classes and methods
8. inversion of control through block-taking messages
9. domain objects
10. DSL messages that capture expert idioms

This works well because the DSL is not a strange jump at the end.

It grows naturally from:

* message syntax
* blocks
* OO ownership of control

---

## 14. What to emphasize to newbies

If the audience is new, the key message is:

* Smalltalk is not about syntax tricks
* Smalltalk is about giving objects responsibility

And the DSL story is:

* once objects own behavior
* and blocks let you pass behavior around
* you can make domain-specific control structures feel natural

So the path is:

* first learn message sends
* then learn blocks
* then see how objects can absorb repeated patterns
* then watch those patterns become a little language

That is the bridge from zero to Smalltalk to DSL.

---

## 15. The big idea

The core Smalltalk habit is this:

* do not start with procedures
* start with objects and messages
* move repeated control patterns into methods
* let users supply just the varying part as blocks

That is why Smalltalk is so good for DSLs.

It turns expert idioms into reusable message protocols, and it lets inversion
of control become a design tool rather than a framework burden.
