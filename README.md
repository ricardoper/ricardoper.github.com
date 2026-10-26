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
- `data/experience.yaml` (technology and electronics together), `data/education.yaml`, `data/awards.yaml`: CV entries, newest first. One block per entry with its three translations side by side. To add an experience, copy a block and edit it.
- `data/certifications.yaml` (certifications from LinkedIn; `featured: true` for the large cards, `badge` for an official badge image) and `data/cert_issuers.yaml` (issuer logos, `static/imgs/certs/`). `data/languages.yaml`: spoken languages shown in "About me".
- `data/links.yaml`: social links (hero and footer).
- `i18n/{en,es,pt}.yaml`: interface texts (menu, hero, about me, labels).
- `layouts/`: the HTML templates (one layout for the three languages).
- `assets/`: CSS and JS (minified and fingerprinted at build time). Sizes use `rem`; from 1600 px of viewport width the root font size grows with the viewport, so the whole page scales on large (4K) screens.
- `static/`: fonts, images, icons, `robots.txt`, `CNAME`. `*.orig.jpg` and `*.full.*` are kept as sources but are not published.
- `mk/`: Makefile fragments. `make header-art` redraws the hero artwork (`scripts/header_art.py`, source `static/imgs/headerBackground.full.svg`) and exports the WebP backgrounds; `make header-photo` builds them from the original photo (`headerBackground.orig.jpg`) instead. `make og-images` rebuilds the social previews (`og-image.{en,es,pt}.jpg`, `scripts/og_images.py`, needs Pillow); run it after changing the hero artwork.
- `hugo.toml`: languages and site configuration.

## Features worth knowing
- **Print / save as PDF**: `Ctrl+P` (or the footer link) produces a clean A4 CV from the same data, in the current language. Folded positions are opened automatically while printing. Styles: `@media print` at the end of `assets/css/style.css`.
- **Dark mode** follows the system preference (`prefers-color-scheme`); the moon/sun button in the menu overrides it and remembers the choice (`localStorage.theme`). Colors of the CV sections are CSS variables defined in the "Color scheme" block of `assets/css/style.css`. **Animations** respect `prefers-reduced-motion`.
- **Earlier positions** (started before `params.foldBefore` in `hugo.toml`, 2014) are folded under "Show earlier positions"; a section always keeps at least its most recent entry visible. Certifications are folded the same way (`params.foldCertsBefore`).
- **Cookies**: Google Analytics (`params.googleAnalytics`) is only loaded after the visitor accepts the notice; the choice is kept in `localStorage` for ~13 months and can be changed from the footer ("Cookies"). The language choice is also kept in `localStorage` (not a cookie).
- **SEO**: JSON-LD `Person` generated from `data/`, `hreflang` alternates, per-language sitemap, trilingual `404.html`.

## Deploy
`.github/workflows/hugo.yaml` builds the site on every push to `main`/`master` and publishes it to GitHub Pages (pull requests are only built, not published).
One-time setup: Settings > Pages > Source must be **GitHub Actions**.
