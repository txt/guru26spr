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


# Prolog Mini-Tutorial

In Prolog, we do not program, we draw.

That is, we do not write a sequence of steps.
We sketch relationships, shapes of truth, and legal moves.
Then Prolog explores that space for us.

You describe:

* what is true
* what follows from what
* what counts as a solution

Prolog handles the search.

Basic conventions:

* atoms start with lowercase: `tim`, `banana`, `parent`
* variables start with uppercase: `X`, `Y`, `Child`
* facts end with `.`
* rules use `:-`, meaning "is true if"

---

## 1. Lists and patterns

Before family trees or search, it helps to see how Prolog "draws" with lists.

A list looks like this:

```prolog
[a, b, c]
```

A list can also be split into:

* a **head**
* a **tail**

Like this:

```prolog
[H|T]
```

So:

```prolog
[a, b, c] = [H|T]
```

means:

* `H = a`
* `T = [b, c]`

This is the key pattern for many Prolog programs.

---

## 2. `member/2`

A classic relation is `member(X, List)`:
`X` is a member of `List`.

You can define it like this:

```prolog
member(X, [X|_]).
member(X, [_|T]) :-
  member(X, T).
```

Read it as:

* `X` is in a list if it is the first thing
* or if it is in the tail

This is a tiny recursive program built from list shapes.

Examples:

```prolog
?- member(b, [a, b, c]).
true.

?- member(X, [a, b, c]).
X = a ;
X = b ;
X = c.
```

So `member/2` is not just a test.
It can also generate answers.

---

## 3. `append/3`

Another classic is `append(A, B, C)`, meaning:

> appending list `A` and list `B` gives list `C`

Definition:

```prolog
append([], L, L).
append([H|T], L, [H|R]) :-
  append(T, L, R).
```

Read it as:

* appending an empty list to `L` gives `L`
* otherwise, keep the head and append the tail

Examples:

```prolog
?- append([a, b], [c, d], X).
X = [a, b, c, d].
```

But also:

```prolog
?- append(X, Y, [a, b, c]).
X = [],
Y = [a, b, c] ;
X = [a],
Y = [b, c] ;
X = [a, b],
Y = [c] ;
X = [a, b, c],
Y = [].
```

This is very "Prolog":

* one relation
* many directions of use

---

## 4. A tiny family database

Now move to facts.

```prolog
parent(tim, pat).
parent(pat, ann).
parent(pat, bob).
parent(ann, liz).
parent(bob, sam).
```

Read `parent(tim, pat).` as:

> Tim is a parent of Pat.

Queries:

```prolog
?- parent(tim, pat).
true.

?- parent(bob, pat).
false.
```

With variables:

```prolog
?- parent(pat, X).
X = ann ;
X = bob.
```

Again, Prolog gives one answer, then backtracks for more.

---

## 5. Defining `grandparent`

Now define a new relation from old ones.

```prolog
grandparent(X, Z) :-
  parent(X, Y),
  parent(Y, Z).
```

This means:

* `X` is a grandparent of `Z`
* if `X` is parent of `Y`
* and `Y` is parent of `Z`

Example:

```prolog
?- grandparent(tim, X).
X = ann ;
X = bob.
```

This is the basic Prolog style:

* state simple facts
* define larger truths from smaller ones

---

## 6. Recursive parent: `ancestor`

Now make the relation recursive.

```prolog
ancestor(X, Y) :-
  parent(X, Y).

ancestor(X, Z) :-
  parent(X, Y),
  ancestor(Y, Z).
```

This says:

* a parent is an ancestor
* if `X` is parent of `Y`, and `Y` is ancestor of `Z`,
  then `X` is ancestor of `Z`

Example:

```prolog
?- ancestor(tim, X).
X = pat ;
X = ann ;
X = bob ;
X = liz ;
X = sam.
```

This is the standard recursive pattern:

* a **base case**
* a **recursive case**

---

## 7. Backtracking

Backtracking is Prolog's built-in search.

```prolog
color(red).
color(green).
color(blue).
```

Query:

```prolog
?- color(X).
X = red ;
X = green ;
X = blue.
```

Prolog tries one match.
If you ask for more (`;`), it backtracks and tries another.

Rules backtrack too:

```prolog
likes(tim, X) :-
  color(X).
```

Then:

```prolog
?- likes(tim, X).
X = red ;
X = green ;
X = blue.
```

So Prolog is always exploring alternatives unless constrained not to.

---

## 8. Monkey and bananas: state-space search

A classic Prolog problem is monkey and bananas.

The monkey wants the banana.
It may need to walk, push a box, climb, then grasp.

We model the world as a state:

```prolog
state(MonkeyPos, BoxPos, Height, HasBanana)
```

Example:

```prolog
state(door, window, floor, no)
```

This means:

* monkey is at `door`
* box is at `window`
* monkey is on the `floor`
* monkey does not have the banana

### Start and goal

```prolog
start(state(door, window, floor, no)).
goal(state(_, _, _, yes)).
```

The goal is any state where the monkey has the banana.

### Legal moves

```prolog
place(door).
place(window).
place(middle).

move(state(P, P, floor, no), climb,
     state(P, P, onbox, no)).

move(state(P1, P1, floor, H), push(P1, P2),
     state(P2, P2, floor, H)) :-
  place(P1), place(P2), P1 \= P2.

move(state(P1, B, floor, H), walk(P1, P2),
     state(P2, B, floor, H)) :-
  place(P1), place(P2), P1 \= P2.

move(state(middle, middle, onbox, no), grasp,
     state(middle, middle, onbox, yes)).
```

This says:

* if monkey and box are together, monkey can climb
* if monkey is on the floor at the box, it can push
* if monkey is on the floor, it can walk
* if monkey is on the box in the middle, it can grasp

---

## 9. Depth-first search

Now let Prolog search for a path.

```prolog
dfs(Path) :-
  start(S),
  ds1(S, [S], Path).

ds1(S, _, []) :-
  goal(S).

ds1(S, Seen, [Act|Path]) :-
  move(S, Act, S1),
  \+ member(S1, Seen),
  ds1(S1, [S1|Seen], Path).
```

What this does:

* start at the initial state
* try a legal move
* avoid revisiting states
* stop when the goal is reached

Example:

```prolog
?- dfs(P).
P = [walk(door, window), push(window, middle), climb, grasp] ;
false.
```

That is a plan.

---

## 10. Iterative deepening

Plain depth-first search can wander too deep down a bad branch.

A neat Prolog trick is to try short paths first.

```prolog
dfid(Path) :-
  between(1, 100, Depth),
  length(Path, Depth),
  dfs(Path).
```

This means:

* try paths of length 1
* then 2
* then 3
* and so on

Because `length(Path, Depth)` fixes the path size, `dfs/1` can only find
paths of that exact depth.

This gives a simple depth-first iterative deepening search.

---

## 11. What naturally comes next?

After this material, the most natural next topic is:

* constraint-based reasoning

Why?

Because you have already seen:

* facts
* rules
* recursion
* backtracking
* state-space search

The next step is to say:

> not all combinations are legal, so let the solver prune impossible choices

That leads to:

* arithmetic constraints
* finite domains
* all-different constraints
* puzzle solving
* scheduling
* configuration

---

## 12. A tiny taste of constraint reasoning

With finite-domain constraints, variables range over legal values.

```prolog
:- use_module(library(clpfd)).

toy([A, B, C, D]) :-
  [A, B, C, D] ins 1..4,
  A #\= B,
  A #\= C,
  B #\= D,
  C #\= D.
```

This says:

* each variable is in `1..4`
* certain pairs must differ

Here:

* `ins` assigns domains
* `#\=` means "must not be equal"

This is still declarative, but smarter: Prolog can rule out bad choices early.

---

## 13. What follows after that?

A very natural next tutorial sequence is:

1. facts and queries
2. list relations like `member/2` and `append/3`
3. family rules like `grandparent/2`
4. recursion with `ancestor/2`
5. backtracking
6. state-space search
7. constraints with `clpfd`
8. toy Sudoku, map coloring, or scheduling

So yes: after the material above, a small constraint tutorial would fit well.

Good next examples:

* map coloring
* mini Sudoku
* simple scheduling
* cryptarithmetic

---

## 14. The big idea

The core Prolog habit is this:

* do not tell the machine what steps to take
* draw the structure of the problem
* let search, unification, and backtracking do the work

That is why `member/2`, `append/3`, family trees, and monkey-bananas all
belong in the same story.

They are all just different shapes of relations.

