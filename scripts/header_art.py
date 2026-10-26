#!/usr/bin/env python3
"""Draws the hero artwork (static/imgs/headerBackground.full.svg).

Four motifs fused left to right, with no text: electronics (PCB traces and chips),
systems (server racks and cabling), software (code windows and a branch graph) and
the cloud (clouds over a node mesh). Flowing threads cross all four, and a Porto
skyline sits at the bottom (the roots). The area behind the hero text is kept calm.
Deterministic: the same script always draws the same image.

    python3 scripts/header_art.py > static/imgs/headerBackground.full.svg   (or: make header-art)
"""
import math
import random

W, H = 3200, 1600
AMBER, TEAL, BLUE, ICE = "#f0a24a", "#19c3c9", "#5b8cff", "#d8f6ff"
INK = "#05090d"
rng = random.Random(1981)
out = []
add = out.append


def zone(i, x0, x1, fade=380):
    """Open a group masked horizontally so neighbouring zones dissolve into each other."""
    add(f'<g mask="url(#m{i})">')


def line(x1, y1, x2, y2, c, w=3, o=.4, extra=""):
    add(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{c}" stroke-width="{w}" stroke-opacity="{o}" {extra}/>')


def poly(pts, c, w=3, o=.4, extra=""):
    p = " ".join(f"{a:.0f},{b:.0f}" for a, b in pts)
    add(f'<polyline points="{p}" fill="none" stroke="{c}" stroke-width="{w}" stroke-opacity="{o}" stroke-linejoin="round" stroke-linecap="round" {extra}/>')


def via(x, y, c, o=.55, r=9):
    add(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{INK}" stroke="{c}" stroke-width="3" stroke-opacity="{o}"/>')


# ---------------------------------------------------------------- defs, background
stops = [(0, 0, 1000), (1, 700, 1700), (2, 1500, 2500), (3, 2200, 3200)]
masks = ""
for i, a, b in stops:
    lo, hi = max(0, a), min(W, b)
    f = 380
    s0 = 0 if lo == 0 else (lo) / W
    s1 = (lo + f) / W if lo else 0
    s2 = (hi - f) / W if hi < W else 1
    s3 = hi / W
    masks += (f'<linearGradient id="g{i}" x1="0" x2="1" y1="0" y2="0" gradientUnits="objectBoundingBox">'
              f'<stop offset="{max(0, lo / W - 0):.3f}" stop-color="#000"/><stop offset="{(lo + f) / W:.3f}" stop-color="#fff"/>'
              f'<stop offset="{(hi - f) / W:.3f}" stop-color="#fff"/><stop offset="{min(1, hi / W):.3f}" stop-color="#000"/></linearGradient>'
              f'<mask id="m{i}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="url(#g{i})"/></mask>')
# first and last zones stay fully visible on their outer edge
masks = masks.replace('<stop offset="0.000" stop-color="#000"/><stop offset="0.119" stop-color="#fff"/>', '<stop offset="0" stop-color="#fff"/><stop offset="0.01" stop-color="#fff"/>')
masks = masks.replace(f'<stop offset="{(3200 - 380) / W:.3f}" stop-color="#fff"/><stop offset="1.000" stop-color="#000"/>', '<stop offset="0.99" stop-color="#fff"/><stop offset="1" stop-color="#fff"/>')

add(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0a0806"/><stop offset=".35" stop-color="#06131a"/><stop offset=".7" stop-color="#071a2e"/><stop offset="1" stop-color="#0b2736"/></linearGradient>
<linearGradient id="thread" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="{AMBER}"/><stop offset=".38" stop-color="{TEAL}"/><stop offset=".7" stop-color="{BLUE}"/><stop offset="1" stop-color="{ICE}"/></linearGradient>
<radialGradient id="gA" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{AMBER}" stop-opacity=".30"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>
<radialGradient id="gT" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{TEAL}" stop-opacity=".26"/><stop offset="1" stop-color="{TEAL}" stop-opacity="0"/></radialGradient>
<radialGradient id="gB" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{BLUE}" stop-opacity=".30"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></radialGradient>
<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="16"/></filter>
{masks}
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<circle cx="380" cy="1000" r="900" fill="url(#gA)"/>
<circle cx="1150" cy="1250" r="800" fill="url(#gT)"/>
<circle cx="2050" cy="300" r="800" fill="url(#gB)"/>
<circle cx="2800" cy="700" r="950" fill="url(#gT)"/>''')

# ---------------------------------------------------------------- 1. electronics
zone(0, 0, 1000)
for y0, up in [(110, False), (330, True), (1010, False), (1230, True), (1400, False)]:
    for k in range(8):
        x = rng.randint(20, 160)
        y = y0 + k * 18
        d = rng.randint(50, 120) * (-1 if up else 1)
        r1, r2 = rng.randint(220, 420), rng.randint(180, 420)
        poly([(x, y), (x + r1, y), (x + r1 + abs(d), y + d), (x + r1 + abs(d) + r2, y + d)], AMBER if k % 4 == 0 else TEAL, o=.2 + .05 * (k % 3))
        via(x + r1 + abs(d) + r2, y + d, AMBER if k % 4 == 0 else TEAL)


def chip(x, y, s, c=TEAL, o=.55):
    pitch = 22
    for i in range(1, int(s // pitch)):
        for (a, b, c2, d) in [(x + i * pitch, y - 14, x + i * pitch, y), (x + i * pitch, y + s, x + i * pitch, y + s + 14),
                              (x - 14, y + i * pitch, x, y + i * pitch), (x + s, y + i * pitch, x + s + 14, y + i * pitch)]:
            line(a, b, c2, d, c, 5, o)
    add(f'<rect x="{x}" y="{y}" width="{s}" height="{s}" rx="12" fill="#09151b" stroke="{c}" stroke-opacity="{o}" stroke-width="3"/>')
    add(f'<rect x="{x + s * .27:.0f}" y="{y + s * .27:.0f}" width="{s * .46:.0f}" height="{s * .46:.0f}" rx="6" fill="{c}" fill-opacity=".14" stroke="{c}" stroke-opacity=".5" stroke-width="2"/>')
    add(f'<circle cx="{x + 24}" cy="{y + 24}" r="6" fill="{AMBER}" fill-opacity=".85"/>')


chip(300, 480, 260)
chip(90, 880, 170, o=.45)
chip(700, 760, 200, AMBER, .5)
for _ in range(46):
    x, y = rng.randint(30, 950), rng.randint(60, 1380)
    if 350 < x < 600 and 450 < y < 800:
        continue
    w, h = (22, 11) if rng.random() < .6 else (11, 22)
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" fill="{AMBER}" fill-opacity=".32" stroke="{AMBER}" stroke-opacity=".5"/>')
add('</g>')

# ---------------------------------------------------------------- 2. systems: racks and cabling
zone(1, 700, 1700)
for k in range(7):                                   # racks along the bottom
    x = 820 + k * 135
    h = rng.randint(230, 400)
    y = 1330 - h
    add(f'<rect x="{x}" y="{y}" width="108" height="{h}" rx="8" fill="#08151b" stroke="{TEAL}" stroke-opacity=".5" stroke-width="3"/>')
    for u in range(int(h // 34) - 1):
        uy = y + 18 + u * 34
        add(f'<rect x="{x + 12}" y="{uy}" width="84" height="22" rx="3" fill="{TEAL}" fill-opacity=".10" stroke="{TEAL}" stroke-opacity=".35" stroke-width="1.5"/>')
        add(f'<circle cx="{x + 84}" cy="{uy + 11}" r="3.5" fill="{rng.choice([TEAL, TEAL, AMBER, "#5cf2a6"])}" fill-opacity=".9"/>')
for k in range(5):                                   # switches along the top
    x = 800 + k * 190
    add(f'<rect x="{x}" y="{rng.randint(90, 150)}" width="150" height="46" rx="6" fill="#08151b" stroke="{TEAL}" stroke-opacity=".45" stroke-width="3"/>')
    for p in range(8):
        add(f'<rect x="{x + 14 + p * 16}" y="{rng.randint(90, 150) * 0 + 108}" width="9" height="9" fill="{TEAL}" fill-opacity=".5" transform="translate(0,{0})"/>')
for k in range(13):                                  # cables from the switches down to the racks
    x1 = 820 + (k % 5) * 190 + 40 + (k // 5) * 12
    x2 = 850 + (k % 7) * 135 + 30
    y2 = 1330 - 300
    add(f'<path d="M{x1} 150 C {x1} 520, {x2} 520, {x2} {y2}" fill="none" stroke="{TEAL if k % 3 else AMBER}" stroke-opacity=".22" stroke-width="3"/>')
add('</g>')

# ---------------------------------------------------------------- 3. software: code windows, branches
zone(2, 1500, 2500)
palette = [TEAL, BLUE, AMBER, "#a08cff", ICE]


def window(x, y, w, h, lines):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#08121c" stroke="{BLUE}" stroke-opacity=".45" stroke-width="3"/>')
    line(x, y + 44, x + w, y + 44, BLUE, 2, .3)
    for i, c in enumerate((AMBER, TEAL, "#5cf2a6")):
        add(f'<circle cx="{x + 24 + i * 22}" cy="{y + 22}" r="6" fill="{c}" fill-opacity=".8"/>')
    ind = 0
    for n in range(lines):
        ly = y + 76 + n * 30
        if ly > y + h - 24:
            break
        ind = max(0, min(3, ind + rng.choice([-1, 0, 0, 1])))
        add(f'<rect x="{x + 20}" y="{ly}" width="26" height="10" rx="3" fill="{ICE}" fill-opacity=".12"/>')
        cx = x + 64 + ind * 36
        for _ in range(rng.randint(1, 4)):
            seg = rng.randint(30, 150)
            if cx + seg > x + w - 24:
                break
            add(f'<rect x="{cx}" y="{ly}" width="{seg}" height="10" rx="3" fill="{rng.choice(palette)}" fill-opacity="{rng.choice([.45, .6, .8])}"/>')
            cx += seg + 12


window(1650, 90, 440, 330, 9)
window(2140, 200, 400, 250, 7)
window(1700, 1130, 420, 290, 8)
window(2190, 1180, 360, 220, 6)
for sym, x, y, s in [("{ }", 1580, 520, 110), ("</>", 2420, 520, 100), ("( )", 1680, 1070, 70), ("=>", 2380, 1110, 70), ("[ ]", 2110, 80, 64)]:
    add(f'<text x="{x}" y="{y}" font-family="DejaVu Sans Mono, monospace" font-weight="700" font-size="{s}" fill="{BLUE}" fill-opacity=".22">{sym.replace("<", "&lt;").replace(">", "&gt;")}</text>')
# branch graph
for b, (cy, c) in enumerate([(1000, TEAL), (1040, BLUE), (1080, AMBER)]):
    pts = [(1560 + i * 90, cy + rng.choice([0, 0, 0])) for i in range(11)]
    poly([(1560, 1000), (1560 + 90, cy), (2450, cy)] if b else [(1560, 1000), (2450, 1000)], c, 3, .3)
    for x, y in pts[1:]:
        if rng.random() < .55:
            add(f'<circle cx="{x}" cy="{cy}" r="8" fill="{INK}" stroke="{c}" stroke-width="3" stroke-opacity=".6"/>')
add('</g>')

# ---------------------------------------------------------------- 4. cloud


def cloud(cx, cy, k, c, o=.6, fill=.10):
    d = (f"M{cx - 120 * k:.0f} {cy + 50 * k:.0f} "
         f"a{62 * k:.0f} {62 * k:.0f} 0 0 1 {16 * k:.0f} {-120 * k:.0f} "
         f"a{86 * k:.0f} {86 * k:.0f} 0 0 1 {160 * k:.0f} {-36 * k:.0f} "
         f"a{74 * k:.0f} {74 * k:.0f} 0 0 1 {116 * k:.0f} {76 * k:.0f} "
         f"a{56 * k:.0f} {56 * k:.0f} 0 0 1 {-16 * k:.0f} {80 * k:.0f} Z")
    add(f'<path d="{d}" fill="{c}" fill-opacity="{fill}" stroke="{c}" stroke-opacity="{o}" stroke-width="{max(3, 4 * k):.1f}" stroke-linejoin="round"/>')


zone(3, 2200, 3200)
big = (2860, 560, 3.2)
nodes = []
for _ in range(70):                                       # mesh around and inside the big cloud
    a, r = rng.uniform(0, 2 * math.pi), rng.uniform(0, 520)
    nodes.append((big[0] + r * math.cos(a) * 1.15, big[1] + r * math.sin(a) * .85, rng.randint(5, 11)))
nodes = [n for n in nodes if 2250 < n[0] < 3180 and 40 < n[1] < 1100]
for i, (x, y, _) in enumerate(nodes):
    for j in sorted(range(len(nodes)), key=lambda j: (nodes[j][0] - x) ** 2 + (nodes[j][1] - y) ** 2)[1:3]:
        line(x, y, nodes[j][0], nodes[j][1], ICE, 2, .20)
cloud(*big[:2], big[2], ICE, .55, .07)
cloud(2420, 250, 1.1, BLUE, .6, .12)
cloud(3050, 180, .9, TEAL, .6, .12)
cloud(2540, 930, 1.3, TEAL, .55, .10)
for x, y, r in nodes:
    add(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r * 2.2:.0f}" fill="{ICE}" fill-opacity=".16" filter="url(#blur)"/>')
    add(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{ICE}" fill-opacity=".8"/>')
for k in range(9):                                        # data streams rising from the skyline
    x = 2300 + k * 105 + rng.randint(-20, 20)
    line(x, 1500, x + rng.randint(-60, 60), 1000 - rng.randint(0, 300), TEAL, 3, .3, 'stroke-dasharray="4 16" stroke-linecap="round"')
add('</g>')

# ---------------------------------------------------------------- flowing threads across the four zones
for k, (y0, amp, ph) in enumerate([(780, 130, 0), (840, 110, 1.2), (900, 150, 2.4), (960, 90, 3.6)]):
    pts = [(x, y0 + amp * math.sin(x / 520 + ph)) for x in range(-40, W + 80, 80)]
    d = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts)
    add(f'<path d="{d}" fill="none" stroke="url(#thread)" stroke-width="{4 - k * .6:.1f}" stroke-opacity="{.5 - k * .08:.2f}" stroke-linecap="round"/>')
    for x, y in pts[4::9]:
        add(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{7 - k}" fill="{INK}" stroke="url(#thread)" stroke-width="3"/>')

# ---------------------------------------------------------------- Porto skyline and bridge
add('<g fill="#030608">')
x = 0
while x < W:
    w = rng.randint(60, 130)
    h = rng.randint(34, 90)
    add(f'<polygon points="{x},{H} {x},{H - h} {x + w / 2:.0f},{H - h - rng.randint(14, 36)} {x + w},{H - h} {x + w},{H}"/>')
    x += w
add('</g>')
DECK = H - 110
add(f'<path d="M1380 {H} Q1600 {DECK - 100} 1820 {H}" fill="none" stroke="#030608" stroke-width="12"/>')
add(f'<line x1="1300" y1="{DECK}" x2="1900" y2="{DECK}" stroke="#030608" stroke-width="10"/>')
for bx in range(1400, 1820, 30):
    t = (bx - 1380) / 440
    ay = H * (1 - t) ** 2 + 2 * (DECK - 100) * t * (1 - t) + H * t ** 2
    add(f'<line x1="{bx}" y1="{ay:.0f}" x2="{bx}" y2="{DECK}" stroke="#030608" stroke-width="3"/>')
for bx in (1380, 1820):
    add(f'<line x1="{bx}" y1="{DECK}" x2="{bx}" y2="{H}" stroke="#030608" stroke-width="12"/>')
for _ in range(170):
    wx, wy = rng.randint(0, W), rng.randint(H - 84, H - 8)
    add(f'<rect x="{wx}" y="{wy}" width="6" height="9" fill="{AMBER}" fill-opacity="{rng.choice([.5, .8, .35])}"/>')
add('</svg>')
print("\n".join(out))
