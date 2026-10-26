# Derived images. Sources are kept in static/imgs/sources/ (and *.full.*) and are never published.
# Requires ImageMagick (the `magick` command) built with WebP and SVG support, and Python 3.

HEADER_ART  := static/imgs/headerBackground.full.svg
ORIG_HEADER := static/imgs/sources/headerBackground.orig.jpg
# The old header photo carried a black layer of ~68% (= multiply by 0.32)
HEADER_DARK := 0.32

.PHONY: header-images header-art header-photo og-images
header-images: header-art ## Regenerate the hero background (normal + HD)

header-art: ## Redraw the hero artwork (scripts/header_art.py) and export it as WebP (normal + HD)
	python3 scripts/header_art.py > $(HEADER_ART)
	magick -background '#05090d' -density 96 $(HEADER_ART) \
		-quality 82 -define webp:method=6 static/imgs/headerBackground.webp
	magick -background '#05090d' -density 123 $(HEADER_ART) -resize 4096x \
		-quality 82 -define webp:method=6 static/imgs/headerBackground-hd.webp

header-photo: $(ORIG_HEADER) ## Alternative: build the hero background from the original photo (Porto at night)
	magick $(ORIG_HEADER) -evaluate Multiply $(HEADER_DARK) -filter Lanczos -resize 3200x \
		-quality 80 -define webp:method=6 static/imgs/headerBackground.webp
	magick $(ORIG_HEADER) -evaluate Multiply $(HEADER_DARK) \
		-quality 80 -define webp:method=6 static/imgs/headerBackground-hd.webp

og-images: static/imgs/headerBackground.webp ## Rebuild the social preview images (og-image.{en,es,pt}.jpg) from the hero artwork. Needs Pillow
	python3 scripts/og_images.py
