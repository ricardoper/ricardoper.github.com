# Ricardo Dos Santos Pereira Webpage
- ricardopereira.es
- ricardoper.github.io

Personal CV site built with [Hugo](https://gohugo.io/). Static, semantic HTML5, no framework: a small vanilla JS file and one CSS file.
Languages: EN (default, `/`), ES (`/es/`) and PT (`/pt/`). The root page picks the language from the browser (`navigator.languages`) unless the visitor already chose one with the selector.
The Hugo version is pinned in `.hugo-version` (used by the Makefile and by the GitHub workflow).

## Page sections
Hero (name, intro, social links) → **About me** (with spoken languages) → **Experience** → **Education** → **Certifications** → **Awards** → footer. The menu has a language dropdown and a light/dark toggle.

## Quick start
```
make              # list all commands
make install-hugo # (once) install the pinned Hugo with Go
make serve        # dev server with live reload -> http://localhost:1313
make build        # production build into public/ (same as the workflow)
make preview      # build and serve public/ like production
make clean        # remove public/ and resources/
```
Image targets (only needed when you change the artwork; the generated files are committed): `make header-art`, `make header-photo`, `make og-images`. They need ImageMagick (`magick`, with WebP and SVG support), Python 3 and, for the social previews, Pillow plus the Open Sans fonts.

## Where to edit things
| What | Where |
|---|---|
| Jobs (technology and electronics together), newest first | `data/experience.yaml` |
| Education, awards | `data/education.yaml`, `data/awards.yaml` |
| Certifications | `data/certifications.yaml` (`featured: true` = large card at the top, `badge` = official badge image in `static/imgs/certs/`) |
| Issuer logos used by certifications without a badge | `data/cert_issuers.yaml` + `static/imgs/certs/` |
| Spoken languages (dots follow LinkedIn's 1-5 scale) | `data/languages.yaml` |
| Social links (hero and footer) | `data/links.yaml` |
| Texts of the interface, hero, "About me", meta description | `i18n/{en,es,pt}.yaml` |
| 404 page texts (one trilingual page) | `data/notfound.yaml` |
| Site settings, languages, fold years, Analytics id | `hugo.toml` |

Every entry in `data/` carries its three translations side by side (`en` / `es` / `pt`); to add one, copy a block and edit it. Proper names (certification titles, technologies) are not translated.

## Structure
- `layouts/`: HTML templates (one layout for the three languages; sections are partials).
- `assets/`: CSS and JS (minified and fingerprinted at build time). Sizes use `rem`; from 1600 px of viewport width the root font size grows with the viewport, so the whole page scales on large (4K) screens.
- `static/`: fonts, images, icons, `robots.txt`, `CNAME`, manifest. `static/imgs/sources/` (originals such as the Porto photo) and any `*.orig.*` / `*.full.*` file are sources and are not published (see the mount in `hugo.toml`).
- `mk/`: Makefile fragments (`hugo.mk`, `images.mk`). `scripts/`: Python that draws the artwork (`header_art.py`) and the social previews (`og_images.py`).
- The LinkedIn data export (`Basic_LinkedInDataExport_*`) is git-ignored; it was the source for certifications, awards and languages.

## Images
- **Hero artwork**: drawn by code, with no text: electronics, systems, software and cloud fused left to right, plus a Porto skyline. `make header-art` runs `scripts/header_art.py` (writes `static/imgs/headerBackground.full.svg`) and exports `headerBackground.webp` (3200x1600) and `headerBackground-hd.webp` (4096x2048). `make header-photo` builds the same two files from the original photo (`static/imgs/sources/headerBackground.orig.jpg`) instead.
- **Text legibility over the artwork**: a dark pool behind the text and a light veil are defined in `--hero-shade` (`#home` in `assets/css/style.css`). Lower the alpha values there to show more of the image.
- **Social previews** (`og-image.{en,es,pt}.jpg`, 1200x630): `make og-images` rebuilds them from the hero artwork, the profile photo and the per-language tagline. Run it after changing the artwork.

## Features worth knowing
- **Print / save as PDF**: `Ctrl+P` (or the footer link) produces a clean A4 CV from the same data, in the current language. Folded items are opened automatically while printing. Styles: `@media print` at the end of `assets/css/style.css`.
- **Dark mode** follows the system preference (`prefers-color-scheme`); the moon/sun button in the menu overrides it and remembers the choice (`localStorage.theme`). Colors of the CV sections are CSS variables in the "Color scheme" block of `assets/css/style.css`. **Animations** respect `prefers-reduced-motion`.
- **Folded items**: positions that started before `params.foldBefore` (2014) and certifications issued before `params.foldCertsBefore` (2021) go under a "Show earlier ..." drawer; awards fold in the same way (the year is set in `layouts/index.html`). A section always keeps at least its most recent entry visible.
- **Cookies**: Google Analytics (`params.googleAnalytics`) is only loaded after the visitor accepts the notice; the choice is kept in `localStorage` for ~13 months and can be changed from the footer ("Cookies"). The language and theme choices are also kept in `localStorage` (not cookies), as a preference the visitor asks for, so they need no consent.
- **SEO**: JSON-LD `Person` generated from `data/`, `hreflang` alternates, per-language sitemap, `robots.txt`, trilingual `404.html`. GitHub Pages serves only the root `/404.html`, so that one page shows the three languages.
- **Accessibility**: skip link, visible focus, `aria-label`s on the menu and language list, decorative images and icons hidden from assistive technology.

## Deploy
`.github/workflows/hugo.yaml` builds the site on every push to `main`/`master` and publishes it to GitHub Pages (pull requests are only built, not published).
One-time setup: Settings > Pages > Source must be **GitHub Actions**.
