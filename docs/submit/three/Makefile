SHELL := /bin/bash
GIT_ROOT := $(shell git rev-parse --show-toplevel 2>/dev/null)
HERE := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

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

sh: ## run my shell
	@-bash --init-file $(HERE)/etc/ell -i

push: ## save to cloud
	@read -p "Reason? " msg; git commit -am "$$msg"; git push; git status

~/tmp/%.html: %.py ~/tmp Makefile
	mkdir -p ~/tmp
	pycco -d ~/tmp $<
