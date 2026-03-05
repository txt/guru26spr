.

Here is the complete tutorial and solution guide for your `todo.md` homework, formatted cleanly in GitHub Flavored Markdown (GFMD).

This guide breaks down each problem, explains the concepts, and provides the exact code to include in your `yourcode.st` file.

---

# Smalltalk Homework Solutions (`yourcode.st`)

This document provides the solutions to the 5 exercises outlined in the assignment. All of these solutions rely on the custom metaprogramming framework defined in `my.st`.

To run these solutions, place all the provided code blocks into a single file named `yourcode.st` and run:

```bash
gst my.st yourcode.st

```

---

## 1b1. Number Collector (`Num`)

**The Goal:** Translate a Lua statistical accumulator into a Smalltalk class using the custom `Magic` base class, which provides auto-initialization and getters/setters.

**The Solution:**
We define the class using `Magic sub:has:`. Then we override `init` to set the starting values (handling the standard $10^{32}$ thresholds for min/max). Finally, we implement `nextPut:` to add single numbers, and `nextPutAll:` to iterate over an array of numbers.

```smalltalk
"Define the Num class with instance variables"
Magic sub: #Num has: 'n mu m2 sd lo hi'.

! Num methods !
init
    self n: 0; 
         mu: 0; 
         m2: 0; 
         sd: 0;
         lo: (10 raisedTo: 32); 
         hi: (-1 * (10 raisedTo: 32)). 
!

nextPut: x
    | d |
    x = '?' ifTrue: [ ^x ].
    
    self n: self n + 1.
    d := x - self mu.
    self mu: self mu + (d / self n).
    self m2: self m2 + (d * (x - self mu)).
    
    x > self hi ifTrue: [ self hi: x ].
    x < self lo ifTrue: [ self lo: x ].
    
    self n >= 2 ifTrue: [
        self sd: (self m2 / (self n - 1 + (10 raisedTo: -32))) sqrt.
    ].
    ^x 
!

nextPutAll: aCollection
    "Iterate over a collection and add each number"
    aCollection do: [:each | self nextPut: each ] 
!
!

```

---

## 1b2. Iterators (`eject:`)

**The Goal:** Write an `eject:` method that does the exact opposite of `select:` (acting like `reject:`), but you must implement it *by calling* `select:`.

**The Solution:**
We add `eject:` to the `Collection` class. It passes the item to the user's block, evaluates it, and then explicitly negates the boolean result using `not`.

```smalltalk
! Collection methods !
eject: aBlock
    "Return elements that do NOT match the block condition"
    ^self select: [:x | (aBlock value: x) not ] 
!
!

```

---

## 1b3. Iterators (`b4Now:`)

**The Goal:** Write an iterator that yields both the previous item (`b4`) and the current item (`now`) to a block.

**The Solution:**
We loop over the collection normally using `do:`. We keep a local variable `b4` to store the previous item. We only execute the block if `b4` is not `nil` (which skips execution on the very first element).

```smalltalk
! Collection methods !
b4Now: block
    | b4 |
    self do: [:now |
        "Only execute the block if we have a previous item"
        b4 notNil ifTrue: [ block value: b4 value: now ].
        
        "Store current item as the previous item for the next loop"
        b4 := now
    ] 
!
!

```

---

## 1b4. Polymorphism (`visit:`)

**The Goal:** Create a generic `visit:` method that walks deeply through objects and collections. Importantly, Smalltalk treats `String` and `Symbol` as collections of characters. We need to stop them from being iterated character-by-character so they print as whole strings/symbols (e.g., `#abc` instead of `$a`, `$b`, `$c`).

**The Solution:**
We define the base behavior on `Object` (visit self), the iterative behavior on `Collection`, and then short-circuit that behavior explicitly on `String` and `Symbol` so they behave like standard objects.

```smalltalk
! Object methods !
visit: aBlock
    "Default behavior: evaluate the block on self"
    ^aBlock value: self 
!

! Collection methods !
visit: aBlock
    "If it's a collection, recursively visit its items"
    self do: [:x | x visit: aBlock ] 
!

! String methods !
visit: aBlock
    "Prevent Strings from being iterated as character arrays"
    ^aBlock value: self 
!

! Symbol methods !
visit: aBlock
    "Prevent Symbols from being iterated as character arrays"
    ^aBlock value: self 
!

```

---

## 1b5. Automated Test Runner (Extra Mark)

**The Goal:** Write a script that dynamically finds all classes, looks for class-side methods in the `'testing'` category, runs them, and safely catches exceptions to tally passes and fails.

**The Solution:**
We use Smalltalk's powerful reflection capabilities (`allSubclasses`, `methodDictionary`, `methodCategory`). We also use exception handling (`on:do:`) so that if a test throws an error (like a division by zero), it gracefully registers as a "fail" and moves on.

```smalltalk
! Object class methods !
runAllTests
    | passes fails total |
    passes := 0.
    fails := 0.

    "Iterate through all subclasses of Object"
    Object allSubclasses do: [:cls |
        
        "Examine the class-side method dictionary"
        cls class methodDictionary keysAndValuesDo: [:selector :method |
            
            "Filter only for methods in the 'testing' category"
            (method methodCategory = 'testing') ifTrue: [
                
                "Try to execute the method using perform:"
                [
                    cls perform: selector.
                    passes := passes + 1.
                ] on: Exception do: [:ex |
                    "If any exception is thrown, it's a failure"
                    fails := fails + 1.
                ].
            ].
        ].
    ].
    
    total := passes + fails.
    Transcript cr; nextPutAll: '=== TEST RESULTS ==='; cr.
    Transcript nextPutAll: 'Total Tests: ', total printString; cr.
    Transcript nextPutAll: 'Passed: ', passes printString; cr.
    Transcript nextPutAll: 'Failed: ', fails printString; cr.
    Transcript nextPutAll: '===================='; cr.
!
!

"Test case to verify our test runner works"
! Num class methodsFor: 'testing' !
goodNum
    | num |
    num := Num new.
    num nextPutAll: #( 2 3 4 4 4 4 5 5 6 7 7 8 9 9 9 9 10 11 12 12).
    ^(num n = 20)
!
!

"Trigger the test runner at the end of the file"
Eval [ Object runAllTests ]

```
