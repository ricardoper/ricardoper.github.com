# Building and serving the site.

.PHONY: check-hugo
check-hugo:
	@command -v $(HUGO) >/dev/null || { echo "hugo not found. Run 'make install-hugo' (needs Go) or see https://gohugo.io/installation/"; exit 1; }
	@v=$$($(HUGO) version | sed -E 's/^hugo v([0-9.]+).*/\1/'); \
	if [ "$$(printf '%s\n%s\n' '$(HUGO_VERSION)' "$$v" | sort -V | head -n1)" != '$(HUGO_VERSION)' ]; then \
		echo "hugo $$v is older than the required $(HUGO_VERSION)"; exit 1; \
	fi

.PHONY: install-hugo
install-hugo: ## Install the Hugo version from .hugo-version with Go
	go install github.com/gohugoio/hugo@v$(HUGO_VERSION)

.PHONY: serve
serve: check-hugo ## Dev server with live reload (http://localhost:1313, or PORT=...)
	$(HUGO) server --port $(PORT) --disableFastRender

.PHONY: build
build: check-hugo ## Production build into public/ (what the workflow runs)
	$(HUGO) --gc --minify --cleanDestinationDir --destination $(PUBLIC_DIR)

.PHONY: preview
preview: build ## Build, then serve public/ like production (PORT=...)
	@echo "Serving $(PUBLIC_DIR)/ at http://localhost:$(PORT)  (Ctrl+C to stop)"
	cd $(PUBLIC_DIR) && python3 -m http.server $(PORT)

.PHONY: clean
clean: ## Remove generated files (public/, resources/)
	rm -rf $(PUBLIC_DIR) resources .hugo_build.lock
