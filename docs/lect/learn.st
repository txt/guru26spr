Transcript nextPutAll: '------------------------------------------------------------------------
 CHUNK 0: Compatibility Extensions (Fixing missing Squeak methods)
------------------------------------------------------------------------'; cr !

"Add missing isZero to Number"
Number extend [
    isZero [
        ^self = 0
    ]
] !

"Add missing valuesDo: to Dictionary (in GST, do: iterates values by default)"
Dictionary extend [
    valuesDo: aBlock [
        self do: aBlock
    ]
] !

"Add missing printStringBase: to Integer (GST uses printString: instead)"
Integer extend [
    printStringBase: base [
        ^self printString: base
    ]
] !

Transcript nextPutAll: '------------------------------------------------------------------------
 CHUNK 1: Output, Assignment, Basic Types, and Constants
------------------------------------------------------------------------'; cr !

Eval [
    | x y b |
    Transcript show: 'Hello World'.
    Transcript nextPutAll: 'Hello World'.
    Transcript nextPut: $A.
    Transcript space; tab; cr.
    'Hello' printOn: Transcript.
    'Hello' storeOn: Transcript.
    Transcript endEntry.

    x := 4.
    x := y := 6. 
    x := (y := 6) + 1.
    x := Object new.

    b := true.
    b := false.
    x := nil.
    x := 1.
    x := 3.14.
    x := 2e-2.
    x := 16r0F.
    x := -1.
    x := 'Hello'.
    x := 'I''m here'.
    x := $A.
    x := $ .
    x := #aSymbol.
    x := #(3 2 1).
    x := #('abc' 2 $a).
] !

Transcript nextPutAll: '------------------------------------------------------------------------
 CHUNK 2: Booleans and Conditionals
------------------------------------------------------------------------'; cr !

Eval [
    | x y b switch result |
    x := 1. y := 2.
    
    b := (x = y).
    b := (x ~= y).
    b := (x == y).
    b := (x ~~ y).
    b := (x > y).
    b := (x < y).
    b := (x >= y).
    b := (x <= y).
    b := b not.
    b := (x < 5) & (y > 1).
    b := (x < 5) | (y > 1).
    b := (x < 5) and: [y > 1].
    b := (x < 5) or: [y > 1].
    b := (x < 5) eqv: (y > 1).
    b := (x < 5) xor: (y > 1).
    b := 5 between: 3 and: 12.
    
    b := 123 isKindOf: Number.
    b := 123 isMemberOf: SmallInteger.
    b := x isNil.
    b := x isZero. "<- Works now thanks to Chunk 0"
    b := x positive.
    b := x strictlyPositive.
    b := x negative.
    b := x even.
    b := x odd.
    b := x isInteger.
    b := x isFloat.
    b := x isNumber.
    b := $A isUppercase.
    b := $A isLowercase.

    x > 10 ifTrue: [Transcript show: 'ifTrue'; cr].
    x > 10 ifFalse: [Transcript show: 'ifFalse'; cr].
    x > 10 ifTrue: [Transcript show: 'ifTrue'; cr] ifFalse: [Transcript show: 'ifFalse'; cr].
    x > 10 ifFalse: [Transcript show: 'ifFalse'; cr] ifTrue: [Transcript show: 'ifTrue'; cr].
    
    switch := Dictionary new.
    switch at: $A put: [Transcript show: 'Case A'; cr].
    switch at: $B put: [Transcript show: 'Case B'; cr].
    switch at: $C put: [Transcript show: 'Case C'; cr].
    result := (switch at: $B) value.
] !

Transcript nextPutAll: '------------------------------------------------------------------------
 CHUNK 3: Arithmetic and Bitwise Operations
------------------------------------------------------------------------'; cr !

Eval [
    | x b rng |
    x := 6 + 3.
    x := 6 - 3.
    x := 6 * 3.
    x := 1 + (2 * 3).
    x := 5 / 3.
    x := 5.0 / 3.0.
    x := 5.0 // 3.0. 
    x := 5.0 \\ 3.0. 
    x := -5.
    x := 5 sign.
    x := 5 negated.
    x := 1.2 integerPart.
    x := 1.2 fractionPart.
    x := 5 reciprocal.
    x := 6 * 3.1.
    x := 5 squared.
    x := 25 sqrt.
    x := 5 raisedTo: 2.
    x := 5 raisedToInteger: 2.
    x := 5 exp.
    x := -5 abs.
    
    "Using 3.5 instead of 3.99 to bypass GST's float printing bug"
    x := 3.5 rounded.
    x := 3.5 truncated.
    x := 3.5 floor.
    x := 3.5 ceiling.
    
    x := 5 factorial.
    x := -5 quo: 3.
    x := -5 rem: 3.
    x := 28 gcd: 12.
    x := 28 lcm: 12.
    x := 100 ln.
    x := 100 log.
    x := 180 degreesToRadians.
    x := 3.14 radiansToDegrees.
    x := 0.7 sin.
    x := 0.7 cos.
    x := 0.7 tan.
    x := 0.7 arcSin.
    x := 0.7 arcCos.
    x := 0.7 arcTan.
    x := 10 max: 20.
    x := 10 min: 20.
    x := Float pi.
    x := Float e.
    
    rng := Random new.
    x := rng next.
    x := rng between: 1 and: 100.

    x := 16rFF bitAnd: 16r0F.
    x := 16rF0 bitOr: 16r0F.
    x := 16rFF bitXor: 16r0F.
    x := 16rFF bitInvert.
    x := 16r0F bitShift: 4.
    x := 16rF0 bitShift: -4.
    x := 16r80 highBit.
    b := 16rFF allMask: 16r0F.
    b := 16rFF anyMask: 16r0F.
    b := 16rFF noMask: 16r0F.
] !

Transcript nextPutAll: '------------------------------------------------------------------------
 CHUNK 4: Conversion, Blocks, Method Calls, Characters
------------------------------------------------------------------------'; cr !

Eval [
    | x y |
    "Using 3.5 to bypass the Float>Fraction bug"
    x := 3.5 asInteger.
    x := 3.5 asFraction.
    x := 3 asFloat.
    x := 65 asCharacter.
    x := $A asciiValue.
    x := 3.5 printString.
    x := 3.5 storeString.
    x := 15 printStringBase: 16.

    x := [ y := 1. y + 1 ].
    x value.
    x := [ :argOne :argTwo | argOne, ' and ' , argTwo ].
    Transcript show: (x value: 'First' value: 'Second'); cr.
    
    x := [ :arg | | local | local := arg + 1. local ].

    x := 2 sqrt.
    x := 2 raisedTo: 10.
    x := 194 * 9.
    Transcript show: (194 * 9) printString; cr.
    x := 2 perform: #sqrt.
    
    Transcript show: 'hello '; show: 'world'; cr. 

    x := $A.
    y := x isLowercase.
    y := x isUppercase.
    y := x isLetter.
    y := x isDigit.
    y := x isAlphaNumeric.
    y := x isSeparator.
    y := x isVowel.
    y := x digitValue.
    y := x asLowercase.
    y := x asUppercase.
    y := x asciiValue.
    y := x asString.
] !

Transcript nextPutAll: '------------------------------------------------------------------------
 CHUNK 5: Iteration and Collections
------------------------------------------------------------------------'; cr !

Eval [
    | x y b sum max dict |
    x := 4. y := 1.
    [x > 0] whileTrue: [x := x - 1. y := y * 2].
    [x >= 4] whileFalse: [x := x + 1. y := y * 2].
    x timesRepeat: [y := y * 2].
    1 to: x do: [:a | y := y * 2].
    1 to: x by: 2 do: [:a | y := y / 2].
    #(5 4 3) do: [:a | x := x + a].

    x := Interval from: 1 to: 5.
    x := Array new: 10.
    x at: 1 put: 'First'.
    y := x at: 1.
    x := ByteArray new: 10.
    x := String new: 10.
    x := Set new.
    x add: 'First'.
    x add: 'Second'.
    x remove: 'First' ifAbsent: [].
    b := x includes: 'First'.
    b := x isEmpty.
    y := x size.
    x := Bag new.
    
    dict := Dictionary new.
    dict at: #Key1 put: 'Value1'.
    dict at: #Key2 put: 'Value2'.
    y := dict keys.
    y := dict values.
    dict keysDo: [:k | k printString].
    dict valuesDo: [:v | v printString]. "<- Works now thanks to Chunk 0"
    dict keysAndValuesDo: [:k :v | k printString. v printString].

    x := #(1 2 3 4 5).
    y := x first.
    y := x last.
    x do: [:a | a printString].
    y := x select: [:a | a > 2].
    y := x reject: [:a | a < 2].
    y := x collect: [:a | a + a].
    y := x detect: [:a | a > 3] ifNone: [0].
    
    sum := x inject: 0 into: [:a :c | a + c].
    max := x inject: 0 into: [:a :c | (a > c) ifTrue: [a] ifFalse: [c]].

    y := x asArray.
    y := x asSet.
    y := x asBag.
    y := x asSortedCollection.
] !

Transcript nextPutAll: '------------------------------------------------------------------------
 CHUNK 6: Streams, Dates, Class Reflection, and Miscellaneous
------------------------------------------------------------------------'; cr !

Eval [
    | ios x b date a |
    ios := ReadStream on: 'Hello read stream'.
    [(x := ios next) notNil] whileTrue: [Transcript nextPut: x].
    Transcript cr.
    ios position: 3.
    x := ios position.
    x := ios next.
    x := ios peek.
    x := ios contents.
    b := ios atEnd.

    ios := ReadWriteStream on: 'Hello read stream'.
    ios position: 0.
    ios nextPutAll: 'Chris'.
    ios position: 0.
    Transcript show: ios contents; cr.

    ios := FileStream open: 'ios.txt' mode: FileStream write.
    ios nextPut: $H; cr.
    ios nextPutAll: 'Hello File'; cr.
    'Hello File' printOn: ios.
    ios close.

    ios := FileStream open: 'ios.txt' mode: FileStream read.
    [(x := ios nextLine) notNil] whileTrue: [Transcript show: x; cr].
    ios close.

    date := Date today.
    
    x := String name.
    x := String comment.
    x := String superclass.
    x := String subclasses.
    x := String allSubclasses.
    x := String allInstances.
    b := String instSize.
    b := String isFixed.
    b := String isVariable.

    x := 1.2 hash.
    y := x shallowCopy.
    y := x deepCopy.
    
    "Literal strings are read-only. We send #copy so become: has mutable objects to swap"
    a := 'A1' copy.
    b := 'B2' copy.
    a become: b. 
] !

Transcript nextPutAll: '------------------------------------------------------------------------
 CHUNK 7: Subclassing & Dynamic Method Calls
------------------------------------------------------------------------'; cr !

Object subclass: Emp [
    | name role |
    
    Emp class >> name: aName role: aRole [
        ^self new initName: aName role: aRole
    ]
    
    initName: aName role: aRole [
        name := aName.
        role := aRole.
        ^self
    ]
    
    name [ ^name ]
    role [ ^role ]
    
    displayOn: aStream [
        aStream nextPutAll: 'Employee[Name: ', name, ', Role: ', role, ']'.
    ]
] !

Eval [
    | argument1 argument2 receiver result worker |
    
    receiver := 12.
    argument1 := 10.
    argument2 := 20.
    
    result := receiver 
        perform: #between:and: 
        withArguments: (Array with: argument1 with: argument2).

    worker := Emp name: 'Ada Lovelace' role: 'Lead Programmer'.
    worker displayNl.
] !
