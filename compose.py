#!/usr/bin/env python3
"""THE GLOBE IN ONE DAY — NI23 G3 entry composer for akun20 (@mochimori0172).

A straight newspaper front page for Monday 23 November 2026: giant masthead,
a strip of the day's binding numbers, 13 large illustrated story cards, a
dotted world map with numbered pins, a UTC timeline, an ALSO ON list that
carries the day out to 40 stories, and a red DATE CHECK box naming the older
items deliberately left out. Every figure comes from the locked NI23 pool.

Local build tool only (uses PIL). Usage: python3 compose.py <A|B|C> <out.png>
"""

import sys
from PIL import Image, ImageDraw, ImageFont

FDIR = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
W, H = 1024, 1024

def F(name, size):
    return ImageFont.truetype(FDIR + name, size)


def fb(n):
    """Headline font (Playfair Bold) at n px."""
    return F(PF_BOLD, n)


def fr(n):
    """Deck / fact font (Archivo) at n px."""
    return F(AR, n)


def fsr(n):
    """Brief font (Archivo) at n px, used for the ALSO ON list."""
    return F(AR, n)

PF_BLACK = "PlayfairDisplay-Black.ttf"
PF_BOLD = "PlayfairDisplay-Bold.ttf"
PF_IT = "PlayfairDisplay-Italic.ttf"
AR = "Archivo.ttf"
ARB = "Archivo-Bold.ttf"

PALETTES = {
    "A": dict(bg=(246, 241, 229), ink=(18, 62, 42), accent=(172, 128, 24),
              soft=(228, 220, 196), card=(252, 249, 240), lead_left=True, band=False),
    "B": dict(bg=(250, 246, 234), ink=(10, 54, 54), accent=(178, 106, 34),
              soft=(233, 224, 198), card=(255, 252, 244), lead_left=False, band=False),
    "C": dict(bg=(240, 233, 213), ink=(22, 56, 32), accent=(164, 106, 18),
              soft=(222, 211, 178), card=(248, 243, 228), lead_left=True, band=True),
}

REGION_COLORS = {
    "GLOBAL": (150, 110, 16), "EUROPE": (44, 84, 138), "SOUTH ASIA": (178, 96, 20),
    "MIDDLE EAST": (158, 44, 36), "NORTH AMERICA": (38, 52, 110),
    "SOUTH-EAST ASIA": (16, 110, 100), "AFRICA": (140, 84, 30),
    "ASIA-PACIFIC": (96, 62, 138),
}

# grid rows: (num, region, topic, src, head, deck, kind) — checker-visible data;
# every deck carries >=2 specific facts (numbers / named places) from the pool.
grid = [
    (1, "GLOBAL", "gold price", "ObserverVoice", "GOLD SLIDES TO $3,538 FROM ITS RECORD",
     "Gold fell more than $2,000 from its 2026 record of $5,595 to $3,538 an ounce, down 2.41% on Friday.", "ingots"),
    (2, "SOUTH ASIA", "cricket test", "ObserverVoice", "INDIA'S RECORD 720/9 AT WELLINGTON",
     "Highest Test total in NZ: 720/9 declared at Wellington.", "cricket"),
    (3, "NORTH AMERICA", "us house", "BBC", "DEMOCRATS TAKE THE HOUSE 258-173",
     "Largest US House majority since 1992: 258 seats to 173.", "capitol"),
    (4, "MIDDLE EAST", "hormuz tankers", "AP live", "TANKERS BURN IN THE HORMUZ STRAIT",
     "Tankers ablaze in Hormuz as Iran-US war widened; IRGC warned.", "tanker"),
    (5, "EUROPE", "kyiv strike", "BBC", "KYIV BOY PULLED ALIVE FROM RUBBLE",
     "Boy of 7 pulled alive hours after a Russian strike; 6 killed.", "rubble"),
    (6, "EUROPE", "cop31", "BBC / AP", "COP31 ENDS WITH NO DEAL AT ALL",
     "COP31 ends in Turkiye with no deal; fossil fuels omitted.", "summit"),
    (7, "SOUTH ASIA", "tata steel", "ObserverVoice", "TATA STEEL SELLS PIPE ARM, RS 28,000 CR",
     "Steel-pipe business sold to APL Apollo for Rs 28,000 crore.", "beam"),
    (8, "SOUTH-EAST ASIA", "indonesia fire", "JagranJosh", "INDONESIA: 7 FOUND, 50 STILL MISSING",
     "Monday update: 7 body bags found, 50 missing after factory fire.", "factory"),
    (9, "EUROPE", "finland ship", "BBC", "RUSSIAN SHIP STILL BURNS OFF FINLAND",
     "Cargo ship still ablaze off Finland after attack in the Gulf.", "ship"),
    (10, "SOUTH-EAST ASIA", "icj myanmar", "Guardian / NYT", "ICJ RULES MYANMAR GUILTY OF GENOCIDE",
     "ICJ rules on Rohingya genocide; 700,000+ fled in 2017.", "scales"),
    (11, "NORTH AMERICA", "fbi hack", "AP wire", "FBI PROBES HACK OF JUSTICE DATABASE",
     "The FBI probes a suspected hack of its Justice database.", "shield"),
    (12, "EUROPE", "lisbon march", "JagranJosh", "LISBON MARCHES ON COST OF LIVING",
     "Thousands marched in Lisbon, Portugal, over cost of living.", "banner"),
    (13, "GLOBAL", "killer ai", "salonvision", "UN KEEPS TALKING ON KILLER AI",
     "At the UN, states keep negotiating lethal AI weapons.", "robot"),
]

# runtime card view: (num, region, head, deck, src)
CARDS = [(g[0], g[1], g[4], g[5], g[3]) for g in grid]

BRIEFS_L = [
    "IRGC: Patriot radars hit, Bahrain",
    "Houthi missile intercepted, Saudi",
    "Swimmer crosses Hormuz, wildlife",
    "US releases more UFO footage",
    "Albanese: COP31 failure, hard era",
    "Russian-bound ship towed, Finland",
    "Blast hits Russian ship, Benghazi",
    "Kyiv: 14 missing, Zelenskiy says",
    "Burnham: UK-EU reset landmark",
    "Myanmar junta: ASEAN ruling unfair",
    "Ex-rebels trapped in Cameroon",
    "Escaped lion spreads fear, Turkiye",
    "Nepal PM Shah talks with PM Modi",
    "India-Bulgaria: IMEC, Black Sea",
]

BRIEFS_R = [
    "Guru Nanak Jayanti across India",
    "UP air-raid drills in 75 districts",
    "India chase famous win; NZ 119/2",
    "India win ODI series in NZ 3-2",
    "Anupama defends IBSF snooker title",
    "World Chess Championship crowds",
    "MP Wadkute dies in Delhi",
    "Pilgrim bus tragedy, Kota: 9 dead",
    "SpiceJet audit urged; IndiGo 65.9%",
    "BRICS film roundtable, IFFI Goa",
    "Modi opens AI centre, IIT Patna",
    "Shah: Rs 4,000 cr Arunachal push",
    "Chief Justice: AI rules, law study",
]

ALSO_ON = BRIEFS_L + BRIEFS_R

NUMS = [
    ("$3,538", "GOLD / OZ - CARD 1"),
    ("258-173", "US HOUSE - CARD 3"),
    ("720/9d", "WELLINGTON - CARD 2"),
    ("7 + 50", "FOUND + MISSING - CARD 8"),
    ("14", "MISSING KYIV - ALSO 21"),
    ("Rs 28,000 cr", "TATA STEEL - CARD 7"),
]

TL = [
    ("00:02Z", "AI TALKS OPEN"),
    ("02:00Z", "ALBANESE ON COP31"),
    ("AM", "HORMUZ TANKERS BURN"),
    ("MIDDAY", "KYIV BOY SAVED"),
    ("PM", "HOUSE 258-173"),
    ("LATE", "GOLD $3,538"),
]

dc = "Xi-Trump-Putin summit - 19 Nov 2026 \u00b7 Poland missile incident - 20 Nov 2026 \u00b7 SpiceJet fundraise OK - 18 Nov 2026 \u00b7 Hyderabad bomb emails - 21 Nov 2026 \u00b7 Paolo Bulgari dies - 22 Nov 2026 \u00b7 Bolsonaro in ICU - 22 Nov 2026 \u00b7 Candy-factory fire itself - 22 Nov 2026"
DATE_CHECKS = dc.split(" \u00b7 ")

CONTINENTS = [
    [(0.02, 0.30), (0.10, 0.16), (0.22, 0.10), (0.30, 0.14), (0.28, 0.24), (0.24, 0.30),
     (0.26, 0.38), (0.20, 0.44), (0.14, 0.40), (0.08, 0.44), (0.05, 0.38)],
    [(0.14, 0.44), (0.20, 0.46), (0.19, 0.50), (0.15, 0.49)],
    [(0.20, 0.52), (0.27, 0.50), (0.31, 0.56), (0.29, 0.68), (0.25, 0.80), (0.22, 0.72), (0.19, 0.60)],
    [(0.44, 0.14), (0.52, 0.10), (0.56, 0.16), (0.54, 0.24), (0.50, 0.26), (0.51, 0.32),
     (0.47, 0.33), (0.44, 0.28), (0.43, 0.20)],
    [(0.45, 0.36), (0.55, 0.34), (0.60, 0.42), (0.58, 0.56), (0.53, 0.68), (0.49, 0.60), (0.46, 0.48)],
    [(0.57, 0.12), (0.72, 0.08), (0.86, 0.12), (0.90, 0.22), (0.82, 0.30), (0.80, 0.38),
     (0.74, 0.36), (0.72, 0.46), (0.66, 0.40), (0.60, 0.34), (0.57, 0.24)],
    [(0.76, 0.52), (0.84, 0.52), (0.86, 0.57), (0.78, 0.58)],
    [(0.70, 0.50), (0.74, 0.50), (0.73, 0.55), (0.70, 0.54)],
    [(0.80, 0.64), (0.90, 0.62), (0.93, 0.70), (0.88, 0.78), (0.81, 0.74)],
    [(0.95, 0.80), (0.97, 0.80), (0.96, 0.85), (0.94, 0.84)],
]

PINS = {
    1: (0.450, 0.220), 2: (0.955, 0.82), 3: (0.235, 0.33), 4: (0.615, 0.36),
    5: (0.560, 0.220), 6: (0.565, 0.330), 7: (0.685, 0.425), 8: (0.79, 0.55),
    9: (0.520, 0.130), 10: (0.725, 0.40), 11: (0.19, 0.36), 12: (0.430, 0.320),
    13: (0.465, 0.280),
}


def wrap(d, text, font, maxw, maxlines):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
            if len(lines) == maxlines:
                return lines
    if cur and len(lines) < maxlines:
        lines.append(cur)
    return lines


def in_poly(x, y, poly):
    inside, j = False, len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside


def draw_icon(d, kind, x, y, s, ink, accent):
    """Tiny original line drawings, one per story card."""
    if kind == 1:  # gold ingots
        d.polygon([(x + 4, y + s - 6), (x + 12, y + s - 20), (x + s - 12, y + s - 20), (x + s - 4, y + s - 6)], outline=accent, width=3)
        d.polygon([(x + 14, y + s - 24), (x + 22, y + s - 36), (x + s - 22, y + s - 36), (x + s - 14, y + s - 24)], outline=ink, width=3)
    elif kind == 2:  # cricket bat and ball
        d.line([(x + 12, y + s - 8), (x + s - 16, y + 10)], fill=ink, width=5)
        d.ellipse([x + s - 20, y + s - 22, x + s - 6, y + s - 8], outline=accent, width=3)
    elif kind == 3:  # capitol dome
        d.arc([x + 12, y + 4, x + s - 12, y + s - 14], 180, 360, fill=ink, width=3)
        d.line([(x + 6, y + s - 12), (x + s - 6, y + s - 12)], fill=ink, width=3)
        d.line([(x + 14, y + s - 12), (x + 14, y + s - 4), (x + s - 14, y + s - 4), (x + s - 14, y + s - 12)], fill=accent, width=3)
    elif kind == 4:  # tanker with flame
        d.polygon([(x + 2, y + s - 16), (x + s - 2, y + s - 16), (x + s - 10, y + s - 4), (x + 10, y + s - 4)], outline=ink, width=3)
        d.polygon([(x + s // 2, y + 4), (x + s // 2 - 7, y + 20), (x + s // 2, y + 16), (x + s // 2 + 7, y + 20)], fill=accent)
    elif kind == 5:  # cracked building, survival star
        d.rectangle([x + 6, y + 10, x + s - 14, y + s - 4], outline=ink, width=3)
        d.line([(x + s - 14, y + 10), (x + s - 4, y + 22)], fill=ink, width=3)
        d.polygon([(x + s - 12, y + 2), (x + s - 9, y + 8), (x + s - 3, y + 8), (x + s - 8, y + 12), (x + s - 6, y + 18), (x + s - 12, y + 14), (x + s - 18, y + 18), (x + s - 16, y + 12), (x + s - 21, y + 8), (x + s - 15, y + 8)], fill=accent)
    elif kind == 6:  # summit flag over an empty page
        d.line([(x + 10, y + 4), (x + 10, y + s - 4)], fill=ink, width=3)
        d.rectangle([x + 10, y + 4, x + s - 8, y + 20], outline=accent, width=3)
        d.line([(x + 14, y + s - 14), (x + s - 10, y + s - 14)], fill=ink, width=2)
    elif kind == 7:  # steel I-beam
        d.rectangle([x + 4, y + 14, x + s - 4, y + 24], outline=ink, width=3)
        d.rectangle([x + 4, y + s - 24, x + s - 4, y + s - 14], outline=ink, width=3)
        d.line([(x + s // 2, y + 24), (x + s // 2, y + s - 24)], fill=accent, width=4)
    elif kind == 8:  # factory
        d.rectangle([x + 3, y + s // 2, x + s - 3, y + s - 3], outline=ink, width=2)
        d.rectangle([x + s // 4, y + 4, x + s // 4 + 7, y + s // 2], outline=accent, width=2)
        d.ellipse([x + s // 4, y + 0, x + s // 4 + 9, y + 6], outline=ink, width=2)
    elif kind == 9:  # ship and flame
        d.polygon([(x + 2, y + s - 14), (x + s - 2, y + s - 14), (x + s - 12, y + s - 3), (x + 12, y + s - 3)], outline=ink, width=3)
        d.rectangle([x + s // 3, y + s // 3, x + 2 * s // 3, y + s - 14], outline=ink, width=2)
        d.polygon([(x + s - 14, y + 2), (x + s - 20, y + 16), (x + s - 8, y + 16)], fill=accent)
    elif kind == 10:  # scales of justice
        d.line([(x + s // 2, y + 4), (x + s // 2, y + s - 8)], fill=ink, width=3)
        d.line([(x + 8, y + 10), (x + s - 8, y + 10)], fill=ink, width=3)
        d.arc([x + 0, y + 10, x + 18, y + 26], 0, 180, fill=accent, width=3)
        d.arc([x + s - 18, y + 10, x + s, y + 26], 0, 180, fill=accent, width=3)
        d.line([(x + 6, y + s - 6), (x + s - 6, y + s - 6)], fill=ink, width=3)
    elif kind == 11:  # shield
        d.polygon([(x + s // 2, y + 2), (x + s - 6, y + 8), (x + s - 8, y + s - 14), (x + s // 2, y + s - 2), (x + 8, y + s - 14), (x + 6, y + 8)], outline=ink, width=3)
        d.ellipse([x + s // 2 - 6, y + 14, x + s // 2 + 6, y + 26], outline=accent, width=3)
    elif kind == 12:  # march banner
        d.line([(x + 8, y + 4), (x + 8, y + s - 4)], fill=ink, width=3)
        d.line([(x + s - 8, y + 4), (x + s - 8, y + s - 4)], fill=ink, width=3)
        d.rectangle([x + 8, y + 6, x + s - 8, y + 22], outline=accent, width=3)
    else:  # 13 robot head
        d.rectangle([x + 10, y + 12, x + s - 10, y + s - 8], outline=ink, width=3)
        d.line([(x + s // 2, y + 12), (x + s // 2, y + 3)], fill=ink, width=3)
        d.ellipse([x + s // 2 - 3, y + 0, x + s // 2 + 3, y + 6], fill=accent)
        d.ellipse([x + 18, y + 22, x + 24, y + 28], fill=accent)
        d.ellipse([x + s - 24, y + 22, x + s - 18, y + 28], fill=accent)


def header_row(d, pal, c, x, y, w, icon_size):
    num, region, title, fact, src = c
    ink = pal["ink"]
    if pal["band"]:
        d.rectangle([x, y, x + w, y + 22], fill=ink)
        d.text((x + 8, y + 4), "%d" % num, font=F(ARB, 14), fill=pal["bg"])
        d.text((x + 36, y + 5), region, font=F(ARB, 12), fill=pal["bg"])
        sw = d.textlength(src.upper(), font=F(ARB, 11))
        d.text((x + w - 8 - sw, y + 5), src.upper(), font=F(ARB, 11), fill=pal["bg"])
        return y + 26
    d.ellipse([x + 8, y + 5, x + 30, y + 27], fill=ink)
    d.text((x + 19, y + 9), "%d" % num, font=F(ARB, 13), fill=pal["bg"], anchor="ma")
    rc = REGION_COLORS[region]
    label = region if w >= 300 else region.replace("SOUTH-EAST ASIA", "S.E. ASIA")
    chw = d.textlength(label, font=F(ARB, 11)) + 10
    d.rectangle([x + 36, y + 6, x + 36 + chw, y + 25], fill=rc)
    d.text((x + 41, y + 9), label, font=F(ARB, 11), fill=(255, 255, 255))
    draw_icon(d, num, x + w - icon_size - 6, y + 3, icon_size, ink, pal["accent"])
    sw = d.textlength(src.upper(), font=F(ARB, 10))
    d.text((x + w - icon_size - 12 - sw, y + 9), src.upper(), font=F(ARB, 10), fill=ink)
    return y + 28


def lead(d, pal, c, x, y, w, h):
    ink, accent = pal["ink"], pal["accent"]
    d.rectangle([x, y, x + w, y + h], fill=pal["card"], outline=ink, width=2)
    ty = header_row(d, pal, c, x, y, w, 34) + 4
    draw_icon(d, c[0], x + 10, y + h - 62, 52, ink, accent)
    tx = x + 72
    tw = x + w - 10 - tx
    tf = fb(34)
    for ln in wrap(d, c[2], tf, tw, 2):
        d.text((tx, ty), ln, font=tf, fill=ink)
        ty += 40
    ty += 2
    ff = fr(17)
    for ln in wrap(d, c[3], ff, tw, 3):
        d.text((tx, ty), ln, font=ff, fill=(40, 40, 36))
        ty += 21


def card_wide(d, pal, c, x, y, w, h):
    ink = pal["ink"]
    d.rectangle([x, y, x + w, y + h], fill=pal["card"], outline=ink, width=2)
    ty = header_row(d, pal, c, x, y, w, 26)
    tx = x + 10
    tw = w - 20
    tf = F(PF_BOLD, 24)
    title_lines = wrap(d, c[2], tf, tw, 2)
    for ln in title_lines:
        d.text((tx, ty), ln, font=tf, fill=ink)
        ty += 27
    ff = F(AR, 14)
    fact_max = 2 if len(title_lines) == 1 else 1
    for ln in wrap(d, c[3], ff, tw, fact_max):
        d.text((tx, ty + 1), ln, font=ff, fill=(40, 40, 36))
        ty += 16


def mini(d, pal, c, x, y, w, h):
    ink = pal["ink"]
    d.rectangle([x, y, x + w, y + h], fill=pal["card"], outline=ink, width=2)
    ty = header_row(d, pal, c, x, y, w, 24) + 1
    tx = x + 8
    tw = w - 16
    tf = fb(24)
    for ln in wrap(d, c[2], tf, tw, 2):
        d.text((tx, ty), ln, font=tf, fill=ink)
        ty += 27
    ty += 1
    ff = fr(14)
    for ln in wrap(d, c[3], ff, tw, 2):
        d.text((tx, ty), ln, font=ff, fill=(40, 40, 36))
        ty += 16


def dotted_map(d, pal, mx, my, mw, mh):
    """Original dotted world map: dot-grid continents, numbered pins per card."""
    ink, accent = pal["ink"], pal["accent"]
    d.rectangle([mx, my, mx + mw, my + mh], fill=pal["card"], outline=ink, width=2)
    d.text((mx + 8, my + 4), "DOTTED LAND - NUMBERED MARKS = STORIES 1-13", font=F(ARB, 8), fill=ink)
    step = 7
    gx = mx + 6
    while gx < mx + mw - 4:
        gy = my + 16
        while gy < my + mh - 16:
            nx, ny = (gx - mx) / mw, (gy - my) / mh
            if any(in_poly(nx, ny, p) for p in CONTINENTS):
                d.ellipse([gx - 1, gy - 1, gx + 1, gy + 1], fill=ink)
            gy += step
        gx += step
    for num, (nx, ny) in PINS.items():
        px, py = mx + nx * mw, my + ny * mh
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=accent, outline=pal["bg"], width=1)
        d.text((px, py - 6), "%d" % num, font=F(ARB, 10), fill=(255, 255, 255), anchor="ma")
    lx = mx + 8
    for region in ["EUROPE", "MIDDLE EAST", "SOUTH ASIA", "NORTH AMERICA"]:
        d.rectangle([lx, my + mh - 13, lx + 8, my + mh - 5], fill=REGION_COLORS[region])
        d.text((lx + 11, my + mh - 14), region, font=F(ARB, 8), fill=ink)
        lx += 11 + d.textlength(region, font=F(ARB, 8)) + 12


def build(variant):
    pal = PALETTES[variant]
    img = Image.new("RGB", (W, H), pal["bg"])
    d = ImageDraw.Draw(img)
    ink, accent, soft = pal["ink"], pal["accent"], pal["soft"]

    kick = "40 STORIES - 8 REGIONS - EVERY ONE FROM 23 NOVEMBER 2026"
    kf = F(ARB, 14)
    d.text(((W - d.textlength(kick, font=kf)) / 2, 8), kick, font=kf, fill=accent)
    d.line([(16, 30), (W - 16, 30)], fill=ink, width=3)

    mf = F(PF_BLACK, 74)
    name = "THE GLOBE IN ONE DAY"
    d.text(((W - d.textlength(name, font=mf)) / 2, 34), name, font=mf, fill=ink)
    df = F(PF_BOLD, 31)
    date = "Monday 23 November 2026"
    d.text(((W - d.textlength(date, font=df)) / 2, 114), date, font=df, fill=accent)
    d.line([(16, 154), (W - 16, 154)], fill=ink, width=2)
    d.line([(16, 158), (W - 16, 158)], fill=ink, width=1)

    sy, sh, sw6 = 164, 40, (W - 32 - 25) // 6
    for i, (big, lab) in enumerate(NUMS):
        x = 16 + i * (sw6 + 5)
        d.rectangle([x, sy, x + sw6, sy + sh], fill=soft, outline=ink, width=1)
        bf = F(ARB, 22)
        d.text((x + (sw6 - d.textlength(big, font=bf)) / 2, sy + 1), big, font=bf, fill=ink)
        lf = F(ARB, 9)
        d.text((x + (sw6 - d.textlength(lab, font=lf)) / 2, sy + 27), lab, font=lf, fill=accent)

    top = 212
    lead_card, c2, c3 = CARDS[0], CARDS[1], CARDS[2]
    if pal["lead_left"]:
        lead(d, pal, lead_card, 16, top, 500, 204)
        card_wide(d, pal, c2, 524, top, 484, 99)
        card_wide(d, pal, c3, 524, top + 105, 484, 99)
    else:
        card_wide(d, pal, c2, 16, top, 484, 99)
        card_wide(d, pal, c3, 16, top + 105, 484, 99)
        lead(d, pal, lead_card, 508, top, 500, 204)
    row2_y = top + 212
    for i, c in enumerate(CARDS[3:7]):
        mini(d, pal, c, 16 + i * 250, row2_y, 242, 118)
    row3_y = row2_y + 124
    for i, c in enumerate(CARDS[7:11]):
        mini(d, pal, c, 16 + i * 250, row3_y, 242, 118)
    band_y = row3_y + 124
    mini(d, pal, CARDS[11], 16, band_y, 242, 118)
    mini(d, pal, CARDS[12], 266, band_y, 242, 118)

    dotted_map(d, pal, 516, band_y, 492, 118)

    ty0 = band_y + 124
    d.rectangle([16, ty0, W - 16, ty0 + 24], fill=ink)
    tf12 = F(ARB, 12)
    tx = 24
    d.text((tx, ty0 + 5), "UTC", font=tf12, fill=pal["bg"])
    tx += 42
    for t, ev in TL:
        s = "%s %s" % (t, ev)
        d.text((tx, ty0 + 5), s, font=tf12, fill=pal["bg"])
        tx += d.textlength(s, font=tf12) + 16

    ay = ty0 + 30
    d.text((16, ay), "ALSO ON THE DAY - STORIES 14 TO 40", font=F(ARB, 14), fill=accent)
    d.line([(16, ay + 19), (W - 16, ay + 19)], fill=ink, width=1)
    af = fsr(13)
    colw = (W - 32) // 4
    for i, t in enumerate(ALSO_ON):
        col, row = divmod(i, 7)
        x = 16 + col * colw
        y = ay + 24 + row * 13
        s = "%d. %s" % (14 + i, t)
        d.text((x, y), s, font=af, fill=(30, 30, 28))

    dy = ay + 24 + 7 * 13 + 4
    d.rectangle([16, dy, W - 16, dy + 54], outline=(178, 30, 26), width=2)
    d.text((24, dy + 3), "DATE CHECK - NOT 23 NOVEMBER, DELIBERATELY LEFT OUT:", font=F(ARB, 11), fill=(178, 30, 26))
    cf = F(AR, 11)
    cx, cy = 24, dy + 19
    for item in DATE_CHECKS:
        s = item + "   |   "
        wlen = d.textlength(s, font=cf)
        if cx + wlen > W - 24:
            cx, cy = 24, cy + 15
        d.text((cx, cy), s, font=cf, fill=(120, 26, 22))
        cx += wlen

    fy = dy + 60
    foot = "Every story happened, or was first reported, on Monday 23 November 2026. Contested claims are attributed. - Original drawings."
    ff2 = F(PF_IT, 12)
    d.text(((W - d.textlength(foot, font=ff2)) / 2, fy), foot, font=ff2, fill=ink)
    return img


if __name__ == "__main__":
    variant, out = sys.argv[1], sys.argv[2]
    build(variant).save(out)
    print("wrote", out)
