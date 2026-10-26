# ricardopereira.es - static site built with Hugo
#
#   make            show this help
#   make serve      work on the site locally (live reload)
#   make build      same build GitHub Actions does -> public/
#
# The Hugo version lives in .hugo-version (also used by the GitHub workflow).
# Override anything on the command line, e.g.  make serve PORT=8080

SHELL := /bin/bash
.DEFAULT_GOAL := help

HUGO_VERSION := $(shell cat .hugo-version)
HUGO         ?= hugo
PORT         ?= 1313
PUBLIC_DIR   ?= public

include mk/hugo.mk
include mk/images.mk

.PHONY: help
help: ## Show this help
	@echo "Usage: make <target>"
	@echo
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z0-9_-]+:.*## / {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
