# # A Tiny Regex Matcher
#
# Rob Pike's elegant regex matcher from
# *Beautiful Code* (Kernighan & Pike, ch.1),
# ported to Python. The whole thing is under 40 lines
# yet handles a useful subset of regular expressions:
#      
# - `c`     : literal character     
# - `.`     : any character     
# - `^`     : start of string     
# - `$`     : end of string     
# - `*`     : zero or more of previous     
#     
# ## The Top-Level Match
#
# If the pattern starts with `^`, we anchor and try only
# position 0. Otherwise we slide a window across the text,
# trying `matchhere` at every starting position.

def match(regex, text):
    if regex and regex[0] == '^':
        return matchhere(regex[1:], text)
    # try every starting position (including empty text)
    for i in range(len(text) + 1):
        if matchhere(regex, text[i:]):
            return True
    return False

# ## The Recursive Core
#
# `matchhere` asks: does `regex` match at exactly this
# point in `text`?  Three cases:
#
# 1. **Empty pattern** — always matches.
# 2. **`c*` pair** — hand off to `matchstar`.
# 3. **`$` at end of pattern** — matches only if text is empty.
# 4. **Literal or `.`** — consume one character and recurse.

def matchhere(regex, text):
    if not regex:
        return True
    if len(regex) >= 2 and regex[1] == '*':
        return matchstar(regex[0], regex[2:], text)
    if regex == '$':
        return text == ''
    if text and (regex[0] == '.' or regex[0] == text[0]):
        return matchhere(regex[1:], text[1:])
    return False

# ## The Star Operator
#
# `matchstar(c, regex, text)` matches `c*` followed by `regex`.
# It tries the **shortest match first** — zero characters,
# then one, then two, etc. This is simple but correct;
# a production engine would use backtracking or an NFA.

def matchstar(c, regex, text):
    # try matching zero, then one, then two...
    i = 0
    while True:
        if matchhere(regex, text[i:]):
            return True
        if i < len(text) and (c == '.' or c == text[i]):
            i += 1
        else:
            return False

# ## Demo
#
# A few quick tests to show it works.

if __name__ == '__main__':
    tests = [
        ('he.lo',  'hello',   True),
        ('^hel',   'hello',   True),
        ('^hel',   'oh hello', False),
        ('lo$',    'hello',   True),
        ('lo$',    'lo and',  False),
        ('ab*c',   'ac',      True),
        ('ab*c',   'abbbbc',  True),
        ('ab*c',   'abbbbd',  False),
        ('.*x',    'abcx',    True),
        ('^..*$',  '',        False),
    ]
    for pat, txt, expected in tests:
        result = match(pat, txt)
        ok = 'ok' if result == expected else 'FAIL'
        print(f"  {ok}  match({pat!r:10s}, {txt!r:10s}) = {result}")
