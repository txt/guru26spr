-- vim: set filetype=lua :
--[[
Python has __doc__ strings (
first string in a name space (a.k.a. file, class, method))
Luas has no such. So we need an excllity var --]]
    local help,trim,fint,str,cli
    help=[[
    poly: demonstrator of DRY, regex
    
    Options:
       -s seed=1 random seed
       -h        show help= 1234567891
       --show    show confif]]
   
-- ACND(all code needs doc). Even you own code will be alien in 3 months time.

    cli={}
    cli["-h"] = function(_) print(help) end

-- First class functions: can be carried around as variables
   -- and those functions also carry around their local variables,

-- OC(Open, closed). Code should for configuration while remining closed for ediit]]

    function trim(s) return s:match"^%s*(.-)%s*$" end
    function cast(s) return math.tointeger(s) or tonumber(s) or str(trim(s)) end
    function str(s)  return s1=="true" and true or (s1 ~= "false" and s1) or false end
    
    help:gsub("\n(%S+)=(%S+)",function(k,v) the[k]=cast(v) end)
   
-- regular expressions: tracintracks to match a patterm
    
