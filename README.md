# Ricardo Dos Santos Pereira Webpage
- ricardopereira.es
- ricardoper.github.io

Static site built with [Hugo](https://gohugo.io/). Languages: EN (default, `/`), ES (`/es/`) and PT (`/pt/`).
The Hugo version is pinned in `.hugo-version` (used by the Makefile and by the GitHub workflow).

## Quick start
```
make              # list all commands
make install-hugo # (once) install the pinned Hugo with Go
make serve        # dev server with live reload -> http://localhost:1313
make build        # production build into public/ (same as the workflow)
make preview      # build and serve public/ like production
```

## Structure
- `data/technology.yaml`, `data/electronics.yaml`, `data/education.yaml`: CV entries, newest first. One block per entry with its three translations side by side. To add an experience, copy a block and edit it.
- `data/links.yaml`: social links (hero and footer).
- `i18n/{en,es,pt}.yaml`: interface texts (menu, hero, about me, labels).
- `layouts/`: the HTML templates (one layout for the three languages).
- `assets/`: CSS and JS (minified and fingerprinted at build time). Sizes use `rem`; from 1600 px of viewport width the root font size grows with the viewport, so the whole page scales on large (4K) screens.
- `static/`: fonts, images, icons, `robots.txt`, `CNAME`. `*.orig.jpg` and `*.full.*` are kept as sources but are not published.
- `mk/`: Makefile fragments. `make header-images` rebuilds the dark header backgrounds from `static/imgs/headerBackground.orig.jpg`.
- `hugo.toml`: languages and site configuration.

## Deploy
`.github/workflows/hugo.yaml` builds the site on every push to `main`/`master` and publishes it to GitHub Pages (pull requests are only built, not published).
One-time setup: Settings > Pages > Source must be **GitHub Actions**.
