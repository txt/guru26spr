"======================================================================
 Homework Solutions for 1b
 Save as: sttut.st
 Run via: gst my.st sttut.st
======================================================================"

"----------------------------------------------------------------------
 BUGFIX: GNU Smalltalk Float Printing Crash
 GST has a known bug where printing Floats like 1.1 causes a ZeroDivide
 exception. We override the 's' method from my.st to catch the crash
 and safely format the string using ScaledDecimal instead.
----------------------------------------------------------------------"
! Float methods !
s
    | fallback |
    ^[ self printString ] on: Exception do: [:ex | 
        "If the GST bug crashes, format safely as a ScaledDecimal"
        fallback := (self asScaledDecimal: 16) printString copyUpTo: $s.
        
        "Trim any trailing zeroes left by ScaledDecimal"
        [ (fallback endsWith: '0') and: [ fallback includes: $. ] ] whileTrue: [
            fallback := fallback copyFrom: 1 to: fallback size - 1.
        ].
        (fallback endsWith: '.') ifTrue: [ fallback := fallback, '0' ].
        fallback
    ]
! !

"----------------------------------------------------------------------
 1b1: Number collector (Num)
----------------------------------------------------------------------"
Magic sub: #Num has: 'n mu m2 sd lo hi'.

! Num methods !
init
    self n: 0; 
         mu: 0; 
         m2: 0; 
         sd: 0;
         lo: 1e32;   "Use scientific float notation"
         hi: -1e32.  "Use scientific float notation"
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
        "Use 1e-32 and the native sqrt method"
        self sd: ((self m2 / (self n - 1 + 1e-32)) sqrt).
    ].
    ^x
!

nextPutAll: aCol
    aCol do: [:x | self nextPut: x ]
! !

"----------------------------------------------------------------------
 1b2: Iterators (eject:)
 Rejecting elements by leveraging the existing select: method.
----------------------------------------------------------------------"
! Collection methods !
eject: aBlock
    ^self select: [:x | (aBlock value: x) not ]
! !

"----------------------------------------------------------------------
 1b3: Iterators (b4Now:)
 Iterator that yields the previous (b4) and current (now) elements.
----------------------------------------------------------------------"
! Collection methods !
b4Now: aBlock
    | b4 |
    self do: [:now |
        b4 notNil ifTrue: [ aBlock value: b4 value: now ].
        b4 := now
    ]
! !

"----------------------------------------------------------------------
 1b4: Polymorphism (visit:)
 Stops Symbols (like #abc) from being broken down into characters ($a $b).
----------------------------------------------------------------------"
! Symbol methods !
visit: aBlock
    ^aBlock value: self
! !

"----------------------------------------------------------------------
 1b5: Automated Test Runner
 Iterates through all classes, finds testing methods, and runs them.
----------------------------------------------------------------------"
! Num class methodsFor: 'testing' !
goodNum
    | num |
    num := Num new.
    num nextPutAll: #( 2 3 4 4 4 4 5 5 6 7 7 8 9 9 9 9 10 11 12 12).
    ^(num n = 20) and: [ num mu = 7 ]
! !

! Object class methods !
runAllTests
    | passes fails |
    passes := 0.
    fails := 0.
    
    Object allSubclasses do: [:cls |
        cls class selectors do: [:sel |
            ((sel asString startsWith: 'good') or: [ (cls class compiledMethodAt: sel) methodCategory = 'testing' ]) ifTrue: [
                [
                    (cls perform: sel) 
                        ifTrue: [ passes := passes + 1 ]
                        ifFalse: [ fails := fails + 1 ].
                ] on: Exception do: [:ex | 
                    fails := fails + 1. 
                ].
            ]
        ]
    ].
    
    Transcript cr; nextPutAll: '=== 1b5 TEST RUN COMPLETE ==='; cr.
    Transcript nextPutAll: 'Passes: ', passes printString; cr.
    Transcript nextPutAll: 'Fails:  ', fails printString; cr.
    Transcript cr.
! !

"======================================================================
 EXECUTION BLOCK 
 Automatically runs the homework output tests when the file is loaded.
======================================================================"
Eval [
    | num |
    
    Transcript nextPutAll: '--- Running 1b1 Tests (Num) ---'; cr.
    num := Num new.
    num nextPutAll: #( 2 3 4 4 4 4 5 5 6 7 7 8 9 9 9 9 10 11 12 12).
    (num sd asScaledDecimal: 2) oo. "==> 3.06"
    num mu oo. "==> 7"
    num n oo.  "==> 20"
    Transcript cr.
    
    Transcript nextPutAll: '--- Running 1b3 Tests (b4Now:) ---'; cr.
    #(10 21 32 43 54) b4Now: [:b4 :now | ((now-b4)/b4) asFloat oo].
    Transcript cr.
    
    Transcript nextPutAll: '--- Running 1b4 Tests (visit:) ---'; cr.
    Object goodVisit. 
    Transcript cr.
    
    Transcript nextPutAll: '--- Running 1b5 Tests (Test Runner) ---'; cr.
    Object runAllTests.
]
