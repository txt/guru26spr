-- vim: set filetype=lua :
-- normally we'd call this file pily.lua
help=[[
poly: demonstrator of DRY, regex

Options:
   -s seed=1 random seed
   -h        show help= 1234567891 ]]

function trim(s) return s:match"^%s*(.-)%s*$" end

function asNum(s) return math.tointeger(s) or tonumber(s)

function asStr(s) 
  s=trim(s); return s1=="true" and true or (s1 ~= "false" and s1) or false end

help:gsub("\n([%s])+([%S]+)",function(x) push(egs.all,x) end)

cli={}
cli["-h"] = function(_) print(help) end

