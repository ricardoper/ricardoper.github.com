# Derived images. Sources are kept in static/imgs/ (*.orig.jpg) and are never published.
# Requires ImageMagick (the `magick` command) built with WebP support.

ORIG_HEADER := static/imgs/headerBackground.orig.jpg
# The header photo carries a black layer of ~68% (= multiply by 0.32)
HEADER_DARK := 0.32

.PHONY: header-images
header-images: $(ORIG_HEADER) ## Regenerate the dark header backgrounds (normal + HD) from the original photo
	magick $(ORIG_HEADER) -evaluate Multiply $(HEADER_DARK) -filter Lanczos -resize 3200x \
		-quality 80 -define webp:method=6 static/imgs/headerBackground.webp
	magick $(ORIG_HEADER) -evaluate Multiply $(HEADER_DARK) \
		-quality 80 -define webp:method=6 static/imgs/headerBackground-hd.webp
