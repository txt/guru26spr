MAKEFLAGS += -s

# target: source ;build		
# run build if source newer than target

# %.md, %.lua				
# matches any file

# >							
# write file

# gawk 'pattern {action}' 	
# patterns laguange (default pattern = True)					

# $<						
# name of first "source"

# $@						
# name of target

# sub
# gawk function returning 1 if a substibution works

# $$0
# How Gawk refers to an entire line inside a Makefile

# luac -p
# lua compiler, parse only looking for errors

%.lua : %.md
	gawk 'sub(/^```.*/,"") { y = 1 - y }  \
	                  	    { print (y ? "" : "-- ") $$0}' $< > $@
	luac -p $@ && lua $@ --$(eg)

