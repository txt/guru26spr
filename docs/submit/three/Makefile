DATA = page_blocks_dirty.csv
SHELL := /bin/bash
GIT_ROOT := $(shell git rev-parse --show-toplevel 2>/dev/null)
HERE := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

all: out/S1 out/S2 out/S3 out/S4 out/S5 \
     out/A out/B out/C out/D out/E out/F \
     out/G out/H out/I out/J out/K out/L out/M

# ── Support ──────────────────────────────────────
help: ## show help.
	@gawk 'BEGIN { FS=":.*##"; \
		printf "\nUsage:\n  make \033[36m<target>\033[0m\n\ntargets:\n" } \
	/^[~a-zA-Z0-9_%./-]+:.*##/ { \
		printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 | "sort" \
	}' $(MAKEFILE_LIST)

banner:
	@printf '\033[36m'
	@printf '%s\n' \
' ______   ______   _____   ______' \
'/\  ___\ /\  __ \ /\  __-. /\  ___\' \
'\ \ \____\ \ \/\ \\ \ \/\ \\ \  __\' \
' \ \_____\\ \_____\\ \____- \ \_____\' \
'  \/_____/ \/_____/ \/____/  \/_____/'
	@printf '\033[0m\n'

date: ## show date
	@date

files: ## show files
	@ls -la

sh: banner ## run my shell
	@-bash --init-file etc/ell -i

push: ## save to cloud
	@read -p "Reason? " msg; git commit -am "$$msg"; git push; git status

~/tmp/%.html: %.py ~/tmp Makefile
	mkdir -p ~/tmp
	pycco -d ~/tmp $<
	echo 'p {text-align: right}' >> ~/tmp/pycco.css

~/tmp:
	mkdir -p ~/tmp

# ── Part 1: gawk ─────────────────────────────────
out/S1: $(DATA); mkdir -p out; gawk -f S1.awk $< > $@
out/S2: $(DATA); mkdir -p out; gawk -f S2.awk $< > $@
out/S3: $(DATA); mkdir -p out; gawk -f S3.awk $< > $@
out/S4: $(DATA); mkdir -p out; gawk -f S4.awk $< > $@
out/S5: $(DATA); mkdir -p out; gawk -f S5.awk $< > $@

# ── Part 2: python ────────────────────────────────
out/A: $(DATA);         mkdir -p out; python3 checks.py A $< > $@
out/B: $(DATA);         mkdir -p out; python3 checks.py B $< > $@
out/C: $(DATA);         mkdir -p out; python3 checks.py C $< > $@
out/D: $(DATA);         mkdir -p out; python3 checks.py D $< > $@
out/E: $(DATA);         mkdir -p out; python3 checks.py E $< > $@
out/F: out/A out/B out/C out/D out/E
	tail -n+2 $^ | grep -vE '^$$|^==>' | sort -u > $@

out/G: $(DATA);         mkdir -p out; python3 checks.py G $< > $@
out/H: $(DATA);         mkdir -p out; python3 checks.py H $< > $@
out/I: $(DATA);         mkdir -p out; python3 checks.py I $< > $@
out/J: $(DATA);         mkdir -p out; python3 checks.py J $< > $@
out/K: $(DATA);         mkdir -p out; python3 checks.py K $< > $@
out/L: out/G out/H out/I out/J out/K
	tail -n+2 $^ | grep -vE '^$$|^==>' | sort -un > $@
out/M: out/G out/H out/I out/J out/K
	tail -n+2 $^ | grep -vE '^$$|^==>' | sort -un > $@
