#!/usr/bin/env python3
"""Builds the social preview images (static/imgs/og-image.{en,es,pt}.jpg, 1200x630).

Background: the hero artwork (static/imgs/headerBackground.webp), darkened; plus the
profile photo, the name, the title and a one-line tagline per language.
Needs Pillow and the Open Sans fonts.   Run it with:  make og-images
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

IMGS = "static/imgs/"
FONTS = "/usr/share/fonts/open-sans/OpenSans-"
W, H = 1200, 630
TAGLINE = {
    "en": "Distributed systems · Cloud · IoT · Electronics",
    "es": "Sistemas distribuidos · Cloud · IoT · Electrónica",
    "pt": "Sistemas distribuídos · Cloud · IoT · Eletrónica",
}
NAME, TITLE, URL = "Ricardo dos Santos Pereira", "Cloud Architect & Software Engineer", "ricardopereira.es"


def font(weight, size):
    return ImageFont.truetype(f"{FONTS}{weight}.ttf", size)


art = Image.open(IMGS + "headerBackground.webp").convert("RGB")
aw, ah = art.size
crop = art.crop((int(aw * .03), 0, int(aw * .03) + int(ah * W / H), ah)).resize((W, H), Image.LANCZOS)
dark = Image.new("RGB", (W, H), (3, 8, 12))
base = Image.blend(crop, dark, .30)
# darker band behind the text, fading to the right
mask = Image.new("L", (W, H), 0)
d = ImageDraw.Draw(mask)
for x in range(W):
    d.line([(x, 0), (x, H)], fill=int(185 * max(0, 1 - max(0, x - 420) / 700)))
base = Image.composite(dark, base, mask.filter(ImageFilter.GaussianBlur(40)))

photo = Image.open(IMGS + "profile.orig.jpg").convert("RGB")
side = min(photo.size)
photo = photo.crop(((photo.width - side) // 2, 0, (photo.width - side) // 2 + side, side)).resize((280, 280), Image.LANCZOS)
circle = Image.new("L", (280, 280), 0)
ImageDraw.Draw(circle).ellipse((0, 0, 279, 279), fill=255)
ring = Image.new("RGB", (296, 296), (25, 195, 201))
ring_mask = Image.new("L", (296, 296), 0)
ImageDraw.Draw(ring_mask).ellipse((0, 0, 295, 295), fill=255)
base.paste(ring, (102, 167), ring_mask)
base.paste(photo, (110, 175), circle)

for lang, tagline in TAGLINE.items():
    img = base.copy()
    t = ImageDraw.Draw(img)
    t.text((452, 198), "Ricardo dos Santos", font=font("Bold", 62), fill="white")
    t.text((452, 268), "Pereira", font=font("Bold", 62), fill="white")
    t.text((452, 352), TITLE, font=font("Semibold", 30), fill=(25, 195, 201))
    t.text((452, 394), tagline, font=font("Regular", 26), fill=(205, 214, 220))
    t.text((452, 470), URL, font=font("Regular", 24), fill=(150, 165, 175))
    img.save(f"{IMGS}og-image.{lang}.jpg", quality=88, optimize=True, progressive=True)
    print("og-image." + lang + ".jpg")
