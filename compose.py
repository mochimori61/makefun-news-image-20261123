#!/usr/bin/env python3
"""THE WORLD IN FULL — NI23 G4 akun20 compose script.

One-day front page, Monday 23 November 2026, 1024x1024.
Lead: thousands march in Lisbon over the cost of living (pool #15).
Trio lead: Lisbon + COP31 ends without a deal + Kyiv boy pulled alive.
38 stories: 13 main cards (3 lead + 10 mini) + 25 briefs.
Variant A = 3-lead row + 5-col grid; variant B = left rail + compact grid.
PIL local only; shipped main.py is stdlib copy-only.
"""
import math
import sys
from PIL import Image, ImageDraw, ImageFont

FDIR = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
W = H = 1024

IVORY = (245, 239, 224)
PAPER = (250, 246, 233)
INK = (20, 67, 46)          # bottle green ink
INK_DARK = (10, 40, 27)
GOLD = (176, 138, 46)       # old gold accent
GOLD_DARK = (146, 112, 32)
RED = (165, 32, 32)
BLACK = (30, 30, 26)
GREY = (96, 96, 88)

REGIONS = {
    "EUROPE": (38, 92, 140),
    "MIDDLE EAST": (178, 84, 30),
    "ASIA-PACIFIC": (120, 62, 140),
    "SOUTH ASIA": (178, 138, 20),
    "NORTH AMERICA": (30, 128, 120),
    "AFRICA": (150, 60, 90),
    "GLOBAL": (90, 90, 90),
}

def F(name, size):
    return ImageFont.truetype(FDIR + name, size)

def pf_black(s): return F("PlayfairDisplay-Black.ttf", s)
def pf_bold(s): return F("PlayfairDisplay-Bold.ttf", s)
def ar_bold(s): return F("Archivo-Bold.ttf", s)
def ar(s): return F("Archivo.ttf", s)
def fb(n): return ar_bold(n)     # headline font helper (fleet style)
def fr(n): return ar(n)          # deck font helper
def fsr(n): return ar(n)         # brief font helper

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

# ------------------------------------------------------------- fleet data
# grid tuples: (num, region, topic, src, head, deck, kind)
grid = [
 (4, "MIDDLE EAST", "WAR · CLAIM", "AP / AFP wires, 23 Nov",
  "IRGC claims radar kill", "IRGC: 2 Patriot radars hit in Bahrain", "radar"),
 (5, "MIDDLE EAST", "WAR AT SEA", "AP live, 23 Nov",
  "Tankers burn at Hormuz", "Tanker ablaze off Hormuz, near Iran", "ship"),
 (6, "EUROPE", "WAR", "JagranJosh, 23 Nov",
  "14 missing, Zelenskiy says", "Drone hit Kyiv block; 14 missing", "drone"),
 (7, "GLOBAL", "AI WEAPONS TALKS", "Salonvision, 23 Nov",
  "UN talks on killer AI", "UN talks: lethal AI rules, Geneva", "robot"),
 (8, "EUROPE", "WAR AT SEA", "BBC / JagranJosh, 23 Nov",
  "Russian ship still burns", "Cargo ship burns off Finland, Baltic Sea", "ship"),
 (9, "EUROPE", "WAR AT SEA", "BBC, 23 Nov",
  "Russia-bound ship towed", "Ship towed after attack in Gulf of Finland", "tow"),
 (10, "AFRICA", "PORT EXPLOSION", "BBC, 23 Nov",
  "Suspected drone strike", "Blast on Russian ship at Benghazi port", "burst"),
 (11, "NORTH AMERICA", "POLITICS", "BBC, 23 Nov",
  "Democrats take House", "Won 258-173 after North Carolina flip", "ballot"),
 (12, "ASIA-PACIFIC", "WORLD COURT", "Guardian / NYT wires, 23 Nov",
  "ICJ: Myanmar genocide", "Myanmar guilty over Rohingya, 2017", "scales"),
 (13, "SOUTH ASIA", "CRICKET", "ObserverVoice, 23 Nov",
  "India declare on 720/9", "720/9 declared vs New Zealand, a record", "bat"),
]
LOCS = {3: "KYIV, UKRAINE",
        4: "BAHRAIN / GULF", 5: "STRAIT OF HORMUZ", 6: "KYIV REGION, UKRAINE",
        7: "GENEVA / WORLDWIDE", 8: "GULF OF FINLAND", 9: "GULF OF FINLAND",
        10: "BENGHAZI, LIBYA", 11: "WASHINGTON, US", 12: "THE HAGUE",
        13: "WELLINGTON, NZ"}
CHIPS = {1: "REPORTED", 2: "OFFICIAL", 3: "REPORTED", 4: "CLAIM", 5: "REPORTED",
         6: "ON RECORD", 7: "ONGOING", 8: "REPORTED", 9: "REPORTED",
         10: "REPORTED", 11: "CONFIRMED", 12: "OFFICIAL", 13: "REPORTED"}

NUMS = [
 ("258-173", "US House, Democrats"),
 ("720/9d", "India's record total"),
 ("14", "missing in Kyiv"),
 ("6", "killed in Kyiv strike"),
 ("$3,538", "gold per ounce"),
 ("65.9%", "IndiGo domestic share"),
]

TL = [
 ("00:02Z", "UN: killer-AI talks to continue"),
 ("02:00Z", "Albanese reacts to COP31"),
 ("MORNING", "COP31 closes, no deal"),
 ("MIDDAY", "Kyiv boy pulled out alive"),
 ("AFTERNOON", "Lisbon cost-of-living march"),
 ("EVENING", "House majority confirmed"),
]

BRIEFS = [
 "14. Houthi missile at Saudi Arabia",
 "15. Swimmer crosses Hormuz Strait",
 "16. US releases more UFO footage",
 "17. Albanese: COP31 a tough era",
 "18. UK-EU reset deal 'landmark'",
 "19. Myanmar slams ASEAN decision",
 "20. Ex-rebels stranded in Cameroon",
 "21. Escaped lion scares Turkiye town",
 "22. Nepal PM Shah meets Modi",
 "23. India, Bulgaria talk IMEC",
 "24. Guru Nanak Jayanti in India",
 "25. UP drills across 75 districts",
 "26. Indonesia fire update: 7, 50",
 "27. India win ODI series 3-2",
 "28. Anupama defends IBSF snooker",
 "29. World Chess final captivates",
 "30. Kota bus tragedy kills 9",
 "31. IndiGo holds 65.9% of market",
 "32. Modi opens AI hub at IIT Patna",
 "33. Google gives $5m to IIT",
 "34. Gold slides to $3,538 ounce",
 "35. Trump attacks Schumer again",
 "36. Hack probe: FBI database hit",
 "37. Miley Cyrus marries Morando",
 "38. Alcaraz beats Zverev in final",
]

dc = ("Xi-Trump-Putin trilateral summit — 19 Nov 2026 · "
      "Russian missiles and drones in Poland — incident 20 Nov · "
      "Paolo Bulgari died — reported 22 Nov 2026 · "
      "24 civilians killed, South Sudan — Juba, 22 Nov · "
      "Ukraine strike on Kerch Bridge — reported 22 Nov · "
      "S. Korea education minister quits — first reported 22 Nov · "
      "Indonesia candy-factory fire AS AN EVENT — 22 Nov (23 Nov update figures only)")

PINS = [(1, .435, .30), (2, .50, .33), (3, .525, .26), (4, .575, .385), (5, .565, .375),
        (6, .525, .25), (7, .478, .285), (8, .512, .185), (9, .515, .19), (10, .498, .355),
        (11, .235, .315), (12, .483, .265), (13, .965, .83)]

REGION_COUNTS = [("EUROPE", 10), ("SOUTH ASIA", 10), ("N. AMERICA", 5),
                 ("MIDDLE EAST", 4), ("ASIA-PACIFIC", 4), ("GLOBAL", 3), ("AFRICA", 2)]

MAPROWS = [
 "          oooo   oooooooooooo              ooo  oooooooooooooooooooooo        ",
 "        ooooooooooooooooooooooo          ooooooooooooooooooooooooooooooo  o   ",
 "         oooooooooooooooooooo      o    ooooooooooooooooooooooooooooooooooo ",
 "          ooooooooooooooooo              oooooooooooooooooooooooooooooooo   ",
 "           ooooooooooooo                  ooooooooooooooooooooooooooooo     ",
 "            oooooooooo        o o          ooooooooooooooooooooooooo        ",
 "             oooooooo        ooooo          oooooooooooooooooooooo          ",
 "              oooooo        ooooooo           ooooooooooooooooo             ",
 "              ooooo          ooooooo           ooooo oooooooo               ",
 "               ooo            ooooo             ooo   ooooo                 ",
 "               oo              ooo               o     ooo        o         ",
 "              ooo              oo                            ooooo          ",
 "              oo               o                              ooo           ",
 "                              o                                            ",
]

# ------------------------------------------------------------------- drawing
def motif(d, x, y, w, h, kind, seed):
    sky = (222, 232, 214) if seed % 2 else (214, 226, 232)
    d.rectangle([x, y, x + w, y + h], fill=sky)
    cx, cy = x + w // 2, y + h // 2
    if kind == "march":
        d.rectangle([x, y + h - 6, x + w, y + h], fill=(150, 140, 110))
        for i, c in enumerate([(178, 84, 30), INK, GOLD, (38, 92, 140)]):
            px = x + 8 + i * (w // 4)
            d.line([px, y + h - 6, px, y + 5], fill=BLACK, width=2)
            d.polygon([(px, y + 5), (px + 14, y + 8), (px, y + 13)], fill=c)
    elif kind in ("ship", "tow"):
        d.rectangle([x, y + h - 9, x + w, y + h], fill=(52, 110, 150))
        d.polygon([(x + 10, y + h - 11), (x + w - 8, y + h - 11), (x + w - 18, y + h - 19), (x + 18, y + h - 19)], fill=(70, 70, 70))
        d.rectangle([cx - 10, y + h - 28, cx + 6, y + h - 19], fill=(120, 120, 120))
        d.polygon([(cx, y + 4), (cx - 5, y + 15), (cx + 2, y + 13), (cx - 1, y + 19), (cx + 6, y + 14)], fill=(230, 120, 30))
    elif kind == "sun":
        d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], outline=GOLD_DARK, width=3)
        for a in range(0, 360, 45):
            dx, dy = int(14 * math.cos(a * math.pi / 180)), int(14 * math.sin(a * math.pi / 180))
            d.line([cx + dx, cy + dy, cx + int(dx * 1.3), cy + int(dy * 1.3)], fill=GOLD_DARK, width=2)
    elif kind == "rubble":
        d.polygon([(x + 6, y + h - 4), (cx, y + 8), (x + w - 6, y + h - 4)], fill=(130, 120, 105))
        d.polygon([(cx - 6, y + h - 4), (cx + 5, y + 15), (x + w - 12, y + h - 4)], fill=(105, 96, 84))
        d.ellipse([cx - 3, y + 13, cx + 3, y + 19], fill=(240, 200, 150))
    elif kind == "radar":
        d.arc([cx - 13, cy - 13, cx + 13, cy + 13], 200, 330, fill=INK, width=3)
        d.arc([cx - 7, cy - 7, cx + 7, cy + 7], 200, 330, fill=GOLD_DARK, width=2)
        d.line([cx, cy + 11, cx, cy - 1], fill=BLACK, width=2)
        d.ellipse([cx + 8, cy - 10, cx + 12, cy - 6], fill=RED)
    elif kind == "drone":
        d.line([cx - 13, cy, cx + 13, cy], fill=BLACK, width=3)
        d.line([cx, cy - 6, cx, cy + 6], fill=BLACK, width=3)
        for dx, dy in [(-13, 0), (13, 0), (0, -6), (0, 6)]:
            d.ellipse([cx + dx - 3, cy + dy - 3, cx + dx + 3, cy + dy + 3], outline=BLACK, width=2)
    elif kind == "robot":
        d.rectangle([cx - 10, cy - 10, cx + 10, cy + 10], outline=INK, width=3)
        d.ellipse([cx - 6, cy - 4, cx - 2, cy], fill=RED)
        d.ellipse([cx + 2, cy - 4, cx + 6, cy], fill=RED)
        d.line([cx - 5, cy + 5, cx + 5, cy + 5], fill=INK, width=2)
    elif kind == "burst":
        for a in range(0, 360, 30):
            dx, dy = int(12 * math.cos(a * math.pi / 180)), int(12 * math.sin(a * math.pi / 180))
            d.line([cx, cy, cx + dx, cy + dy], fill=(200, 90, 20), width=3)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(240, 170, 50))
    elif kind == "ballot":
        d.rectangle([cx - 13, cy - 6, cx + 13, cy + 10], outline=INK, width=3)
        d.rectangle([cx - 8, cy - 13, cx + 8, cy - 5], fill=PAPER, outline=INK, width=2)
        d.line([cx - 5, cy - 10, cx + 4, cy - 7], fill=RED, width=2)
    elif kind == "scales":
        d.line([cx, cy - 13, cx, cy + 11], fill=INK, width=3)
        d.line([cx - 13, cy - 10, cx + 13, cy - 10], fill=INK, width=2)
        d.arc([cx - 16, cy - 10, cx - 6, cy + 3], 0, 180, fill=GOLD_DARK, width=2)
        d.arc([cx + 6, cy - 10, cx + 16, cy + 3], 0, 180, fill=GOLD_DARK, width=2)
    elif kind == "bat":
        d.line([cx - 11, cy + 11, cx + 6, cy - 9], fill=(150, 105, 50), width=5)
        d.ellipse([cx + 5, cy - 13, cx + 12, cy - 6], fill=(200, 40, 40))
    else:
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=INK, width=3)

D = None  # active ImageDraw, set by build()

def lead(x, y, w, h, num, loc, region, src, head, deck, kind, chip, cat):
    d = D
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=INK, width=2)
    d.rectangle([x, y, x + w, y + 17], fill=REGIONS[region])
    d.text((x + 5, y + 2), "%d · %s" % (num, loc), font=ar_bold(12), fill=(255, 255, 255))
    motif(d, x + 4, y + 20, w - 8, 24, kind, num)
    yy = y + 46
    cf = ar_bold(11)
    cw_ = d.textlength(chip, font=cf) + 10
    d.rectangle([x + 5, yy, x + 5 + cw_, yy + 15], fill=GOLD)
    d.text((x + 10, yy + 1), chip, font=cf, fill=(30, 24, 8))
    d.text((x + 12 + cw_, yy + 1), cat, font=ar_bold(11), fill=GREY)
    yy += 17
    for ln in wrap(d, head, fb(28), w - 10)[:2]:
        d.text((x + 5, yy), ln, font=fb(28), fill=INK_DARK); yy += 26
    for ln in wrap(d, deck, fr(15), w - 10)[:2]:
        d.text((x + 5, yy), ln, font=fr(15), fill=BLACK); yy += 16
    d.text((x + 5, yy + 1), "Source: " + src, font=ar(11), fill=GREY)

def mini(d, x, y, w, h, num, region, topic, src, head, deck, kind, compact=False):
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=INK, width=2)
    d.rectangle([x, y, x + w, y + 17], fill=REGIONS[region])
    d.text((x + 5, y + 2), "%d · %s" % (num, LOCS[num]), font=ar_bold(12), fill=(255, 255, 255))
    if compact:
        yy = y + 20
        chip = CHIPS[num]
        cf = ar_bold(10)
        cw_ = d.textlength(chip, font=cf) + 8
        d.rectangle([x + 5, yy, x + 5 + cw_, yy + 13], fill=GOLD)
        d.text((x + 9, yy), chip, font=cf, fill=(30, 24, 8))
        d.text((x + 11 + cw_, yy), topic, font=ar_bold(10), fill=GREY)
        yy += 15
        for ln in wrap(d, head, fb(21), w - 10)[:2]:
            d.text((x + 5, yy), ln, font=fb(21), fill=INK_DARK); yy += 22
        for ln in wrap(d, deck, fr(13), w - 10)[:1]:
            d.text((x + 5, yy), ln, font=fr(13), fill=BLACK); yy += 15
        d.text((x + 5, yy), "Source: " + src, font=ar(10), fill=GREY)
        return
    motif(d, x + 4, y + 20, w - 8, 14, kind, num)
    yy = y + 36
    chip = CHIPS[num]
    cf = ar_bold(11)
    cw_ = d.textlength(chip, font=cf) + 10
    d.rectangle([x + 5, yy, x + 5 + cw_, yy + 15], fill=GOLD)
    d.text((x + 10, yy + 1), chip, font=cf, fill=(30, 24, 8))
    d.text((x + 12 + cw_, yy + 1), topic, font=ar_bold(11), fill=GREY)
    yy += 17
    for ln in wrap(d, head, fb(25), w - 10)[:2]:
        d.text((x + 5, yy), ln, font=fb(25), fill=INK_DARK); yy += 26
    for ln in wrap(d, deck, fr(15), w - 10)[:2]:
        d.text((x + 5, yy), ln, font=fr(15), fill=BLACK); yy += 16
    d.text((x + 5, yy + 1), "Source: " + src, font=ar(11), fill=GREY)

def dotted_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(233, 238, 226), outline=INK, width=2)
    d.text((x + 6, y + 4), "WHERE IT HAPPENED — pins = card numbers", font=ar_bold(12), fill=INK)
    cols = len(MAPROWS[0]); rows = len(MAPROWS)
    gx = (w - 12) / cols; gy = (h - 32) / rows
    for r, row in enumerate(MAPROWS):
        for i, ch in enumerate(row):
            if ch == "o":
                px, py = x + 6 + i * gx, y + 24 + r * gy
                d.ellipse([px, py, px + 2.6, py + 2.6], fill=(120, 140, 110))
    for n, fx, fy in PINS:
        px, py = x + 6 + fx * (w - 12), y + 24 + fy * (h - 32)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED)
        t = str(n); tw = d.textlength(t, font=ar_bold(9))
        d.text((px - tw / 2, py - 5), t, font=ar_bold(9), fill=(255, 255, 255))
    d.text((x + 6, y + h - 15), "Dots mark the land · numbered pins mark the stories", font=ar(11), fill=GREY)

def header(d):
    d.rectangle([0, 0, W, 26], fill=INK)
    d.text((12, 5), "THE WORLD IN FULL", font=ar_bold(13), fill=(245, 239, 224))
    k = "38 STORIES · 7 REGIONS · EVERY ONE FROM 23 NOVEMBER 2026"
    d.text((W - 12 - d.textlength(k, font=ar_bold(13)), 5), k, font=ar_bold(13), fill=GOLD)
    f = pf_black(72)
    t = "Monday 23 November 2026"
    d.text(((W - d.textlength(t, font=f)) / 2, 30), t, font=f, fill=INK_DARK)
    nf = pf_bold(30)
    n = "THE WORLD IN FULL"
    d.text(((W - d.textlength(n, font=nf)) / 2, 106), n, font=nf, fill=INK)
    sub = "Thousands march in Lisbon over living costs · COP31 ends without a deal · Kyiv boy pulled alive from the rubble"
    sf = ar_bold(14)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 140), sub, font=sf, fill=(150, 40, 30))
    yy = 162; xx = 12
    for name, cnt in REGION_COUNTS:
        col = REGIONS.get(name, GREY)
        if name == "N. AMERICA": col = REGIONS["NORTH AMERICA"]
        label = "%s %d" % (name, cnt)
        tw = d.textlength(label, font=ar_bold(12)) + 14
        d.rectangle([xx, yy, xx + tw, yy + 18], fill=col)
        d.text((xx + 7, yy + 2), label, font=ar_bold(12), fill=(255, 255, 255))
        xx += tw + 6
    yy = 186; xx = 12
    d.text((xx, yy + 2), "UTC", font=ar_bold(12), fill=INK); xx += 34
    for tm, ev in TL:
        label = "%s %s" % (tm, ev)
        tw = d.textlength(label, font=ar(11)) + 12
        if xx + tw > W - 12: break
        d.rectangle([xx, yy, xx + tw, yy + 18], outline=GOLD_DARK, width=1)
        d.text((xx + 6, yy + 3), label, font=ar(11), fill=BLACK)
        xx += tw + 5

def numbers_strip(d, x, y, w):
    d.text((x, y - 18), "THE DAY IN NUMBERS", font=ar_bold(14), fill=INK)
    d.rectangle([x, y, x + w, y + 52], fill=(238, 230, 205), outline=GOLD_DARK, width=2)
    cw = w // 6
    for i, (big, lab) in enumerate(NUMS):
        cx = x + i * cw + 8
        d.text((cx, y + 4), big, font=ar_bold(24), fill=(150, 40, 30))
        d.text((cx, y + 32), lab, font=ar(11), fill=BLACK)

def numbers_box_v(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 230, 205), outline=GOLD_DARK, width=2)
    d.text((x + 8, y + 6), "THE DAY IN NUMBERS", font=ar_bold(15), fill=INK)
    yy = y + 30
    for big, lab in NUMS:
        d.text((x + 8, yy), big, font=ar_bold(25), fill=(150, 40, 30)); yy += 27
        d.text((x + 8, yy), lab, font=ar(12), fill=BLACK); yy += 20

def datecheck_box(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(248, 236, 230), outline=RED, width=2)
    d.text((x + 8, y + 4), "DATE CHECK — NOT 23 NOVEMBER NEWS:", font=ar_bold(13), fill=RED)
    yy = y + 24
    for item in dc.split("·"):
        for ln in wrap(d, "· " + item.strip(), ar(11), w - 16)[:2]:
            d.text((x + 8, yy), ln, font=ar(11), fill=BLACK); yy += 12

def also_block(d, x, y, w, cols=5):
    d.text((x, y), "ALSO ON MONDAY 23 NOVEMBER", font=ar_bold(14), fill=INK)
    yy0 = y + 20
    per = (len(BRIEFS) + cols - 1) // cols
    cw = w // cols
    for ci in range(cols):
        yy = yy0
        for b in BRIEFS[ci * per:(ci + 1) * per]:
            d.text((x + ci * cw, yy), b, font=fsr(13), fill=BLACK)
            yy += 17

def footer(d, y):
    d.line([12, y, W - 12, y], fill=GOLD_DARK, width=2)
    lines = [
        "HOW SURE: REPORTED = named source · CLAIM = one side's account, labelled · ONGOING = still developing · OFFICIAL / ON RECORD / CONFIRMED = stated by the body named.",
        "Every story happened, or was first reported, on Monday 23 November 2026. Contested claims are attributed. Original drawings.",
    ]
    yy = y + 5
    for ln in lines:
        for wln in wrap(d, ln, ar(11), W - 24):
            d.text((12, yy), wln, font=ar(11), fill=GREY); yy += 13

def build(variant):
    global D
    img = Image.new("RGB", (W, H), IVORY)
    d = ImageDraw.Draw(img)
    D = d
    header(d)
    if variant == "A":
        cw = (W - 24 - 12) // 3
        lead(12, 210, cw, 160, 1, "LISBON, PORTUGAL", "EUROPE",
             "JagranJosh, 23 Nov", "Lisbon marches over living costs",
             "Thousands marched in Lisbon, Portugal over living costs", "march",
             "REPORTED", "PROTEST")
        lead(12 + cw + 6, 210, cw, 160, 2, "ANTALYA, TURKIYE", "EUROPE",
             "BBC / AP, 23 Nov", "COP31 ends without a deal",
             "Final Turkish draft omitted 'fossil fuels'; no deal in Antalya", "sun",
             "OFFICIAL", "CLIMATE SUMMIT")
        lead(12 + 2 * (cw + 6), 210, cw, 160, 3, "KYIV, UKRAINE", "EUROPE",
             "BBC, 23 Nov", "Boy, 7, pulled alive from rubble",
             "Boy, 7, freed after hours in Kyiv rubble; 6 killed", "rubble",
             "REPORTED", "WAR")
        gw = (W - 24 - 24) // 5
        for i, t in enumerate(grid):
            r, col = divmod(i, 5)
            mini(d, 12 + col * (gw + 6), 376 + r * 156, gw, 150,
                 t[0], t[1], t[2], t[3], t[4], t[5], t[6])
        also_block(d, 12, 690, W - 24)
        numbers_strip(d, 12, 819, W - 24)
        dotted_map(d, 12, 877, 470, 112)
        datecheck_box(d, 490, 877, 522, 112)
        footer(d, 995)
    else:
        # Variant B: left rail (numbers + map + date check), 2 lead cards,
        # compact grid on the right, ALSO ON full width at the bottom.
        numbers_box_v(d, 12, 210, 300, 240)
        dotted_map(d, 12, 456, 300, 172)
        datecheck_box(d, 12, 634, 300, 192)
        cw2 = (700 - 6) // 2
        lead_args = [
            (1, "LISBON, PORTUGAL", "EUROPE", "JagranJosh, 23 Nov",
             "Lisbon marches over living costs",
             "Thousands marched in Lisbon, Portugal over living costs", "march",
             "REPORTED", "PROTEST"),
            (2, "ANTALYA, TURKIYE", "EUROPE", "BBC / AP, 23 Nov",
             "COP31 ends without a deal",
             "Final Turkish draft omitted 'fossil fuels'; no deal in Antalya", "sun",
             "OFFICIAL", "CLIMATE SUMMIT"),
        ]
        for j, a in enumerate(lead_args):
            lead(324 + j * (cw2 + 6), 210, cw2, 160, *a)
        gw = (700 - 12) // 3
        rest = [(3, "EUROPE", "WAR", "BBC, 23 Nov", "Boy, 7, pulled alive from rubble",
                 "Boy, 7, freed after hours in Kyiv rubble; 6 killed", "rubble")] + grid
        for i, t in enumerate(rest):
            r, col = divmod(i, 3)
            mini(d, 324 + col * (gw + 6), 376 + r * 110, gw, 104,
                 t[0], t[1], t[2], t[3], t[4], t[5], t[6], compact=True)
        also_block(d, 12, 838, W - 24, cols=5)
        footer(d, 950)
    return img

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "A"
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/ni23g4-akun20-A.png"
    build(which).save(out, optimize=True)
    print(out)
