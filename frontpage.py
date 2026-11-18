"""Draw the round-2 front page for make.fun news-image-20261118.

A dense broadsheet edition of the world news of Wednesday
18 November 2026: nine numbered story cards with flat-illustration
strips, a "by the numbers" strip, a dotted world map with pins for
the card stories, and a numbered index of six more stories. Every
fact is one of the day's verified reports listed in the README.

Drawn at twice size with Pillow and downscaled, so type and edges
stay smooth. Output is deterministic: same bytes on every run.

Run:  python3 frontpage.py   ->  writes entry.png beside this file
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
S = 2                      # supersample factor
W = H = 1024               # final size

# ---------------------------------------------------------------- palette
PAGE = (244, 238, 226)
CARD = (253, 251, 244)
INK = (24, 24, 22)
NAVY = (16, 38, 66)
NAVY_D = (10, 24, 44)
RED = (172, 28, 44)
RED_D = (128, 20, 34)
GOLD = (190, 148, 70)
GREY = (104, 99, 89)
FAINT = (140, 134, 120)
LINE = (199, 189, 165)
TEAL = (24, 92, 96)
GREEN_D = (10, 34, 26)
SAND = (226, 205, 164)

DISPLAY = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, int(size * S))


def u(v):
    return int(round(v * S))


# ---------------------------------------------------------------- helpers
def wrap(draw, text, font, width):
    """Greedy word wrap to a pixel width given in final-size points."""
    width = u(width)
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def tracked(draw, x, y, text, font, fill, tracking=2.2, right=None):
    """Letter-spaced small caps; returns the end x (final-size points)."""
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = (sum(widths) + u(tracking) * (len(text) - 1)) / S
    if right is not None:
        x = right - total
    cx = u(x)
    for ch, w in zip(text, widths):
        draw.text((cx, u(y)), ch, font=font, fill=fill)
        cx += int(w) + u(tracking)
    return x + total


def text(draw, x, y, s, font, fill=INK):
    draw.text((u(x), u(y)), s, font=font, fill=fill)


def rect(draw, box, fill=None, outline=None, width=1):
    box = [u(v) for v in box]
    draw.rectangle(box, fill=fill, outline=outline, width=u(width))


def line(draw, pts, fill=INK, width=1):
    draw.line([u(v) for v in pts], fill=fill, width=u(width))


def ellipse(draw, box, fill=None, outline=None, width=1):
    draw.ellipse([u(v) for v in box], fill=fill, outline=outline, width=u(width))


# ------------------------------------------------------- illustration strips
def illo_shenzhen(d, x, y, w, h):
    """Dusk skyline, a gold sun, one small plane."""
    for i in range(u(h)):
        t = i / u(h)
        c = tuple(int(NAVY_D[j] + (86 - NAVY_D[j]) * t) for j in range(3))
        d.line([(u(x), u(y) + i), (u(x + w), u(y) + i)], fill=c)
    ellipse(d, [x + w - 62, y + 8, x + w - 22, y + 48], fill=GOLD)
    towers = [(0, 30, 26, 40), (30, 18, 20, 52), (54, 36, 30, 34),
              (88, 10, 16, 60), (108, 28, 24, 42), (136, 20, 14, 50),
              (154, 34, 30, 36), (188, 14, 18, 56), (210, 30, 26, 40),
              (240, 24, 16, 46), (260, 38, 28, 32)]
    for tx, ty, tw, th in towers:
        rect(d, [x + tx * w / 288, y + h - th, x + (tx + tw) * w / 288, y + h],
             fill=(8, 18, 34))
    for wx, wy in [(36, 44), (96, 30), (196, 36), (222, 52), (60, 56)]:
        rect(d, [x + wx * w / 288, y + wy, x + wx * w / 288 + 3, y + wy + 4],
             fill=(255, 214, 130))
    d.polygon([(u(x + 18), u(y + 12)), (u(x + 34), u(y + 16)),
               (u(x + 18), u(y + 20))], fill=(230, 230, 225))


def illo_gulf(d, x, y, w, h):
    """A tanker on a pale sea, two drones above."""
    rect(d, [x, y, x + w, y + h * 0.52], fill=(214, 222, 224))
    rect(d, [x, y + h * 0.52, x + w, y + h], fill=(52, 96, 116))
    ellipse(d, [x + 16, y + 8, x + 40, y + 32], fill=GOLD)
    hull_y = y + h * 0.52
    d.polygon([(u(x + 60), u(hull_y)), (u(x + 210), u(hull_y)),
               (u(x + 196), u(hull_y + 14)), (u(x + 74), u(hull_y + 14))],
              fill=(30, 30, 34))
    rect(d, [x + 88, hull_y - 12, x + 168, hull_y], fill=(120, 44, 40))
    rect(d, [x + 176, hull_y - 18, x + 190, hull_y], fill=RED_D)
    d.polygon([(u(x + 179), u(hull_y - 18)), (u(x + 183), u(hull_y - 27)),
               (u(x + 187), u(hull_y - 18))], fill=(232, 128, 40))
    d.polygon([(u(x + 181), u(hull_y - 18)), (u(x + 183), u(hull_y - 23)),
               (u(x + 185), u(hull_y - 18))], fill=(246, 190, 70))
    for dx, dy in [(236, 14), (262, 26)]:
        line(d, [x + dx - 7, y + dy - 7, x + dx + 7, y + dy + 7], fill=INK, width=2)
        line(d, [x + dx - 7, y + dy + 7, x + dx + 7, y + dy - 7], fill=INK, width=2)


def illo_ukraine(d, x, y, w, h):
    """A grey, broken skyline under smoke."""
    rect(d, [x, y, x + w, y + h], fill=(196, 196, 192))
    blocks = [(0, 26, 34), (36, 40, 26), (66, 20, 44), (114, 34, 30),
              (148, 24, 40), (192, 38, 28), (224, 22, 42), (270, 32, 32)]
    for bx, bh, bw in blocks:
        rect(d, [x + bx * w / 302, y + h - bh, x + (bx + bw) * w / 302, y + h],
             fill=(88, 88, 90))
    d.polygon([(u(x + 66 * w / 302), u(y + h - 20)), (u(x + 84 * w / 302), u(y + h - 34)),
               (u(x + 100 * w / 302), u(y + h - 20))], fill=(196, 196, 192))
    for i in range(4):
        ellipse(d, [x + 120 + i * 16, y + 6 + i * 2, x + 152 + i * 16, y + 22 + i * 2],
                fill=(150, 150, 148))
    rect(d, [x, y + h - 5, x + w, y + h], fill=(70, 70, 72))


def illo_nvidia(d, x, y, w, h):
    """A chip and rising bars on near-black green."""
    rect(d, [x, y, x + w, y + h], fill=GREEN_D)
    cx, cy, cs = x + 44, y + h / 2, 40
    rect(d, [cx - cs / 2, cy - cs / 2, cx + cs / 2, cy + cs / 2],
         outline=(64, 220, 150), width=2)
    rect(d, [cx - 11, cy - 11, cx + 11, cy + 11], outline=(64, 220, 150), width=2)
    for i in range(4):
        px = cx - cs / 2 + 8 + i * 9
        line(d, [px, cy - cs / 2 - 6, px, cy - cs / 2], fill=(64, 220, 150), width=2)
        line(d, [px, cy + cs / 2, px, cy + cs / 2 + 6], fill=(64, 220, 150), width=2)
        py = cy - cs / 2 + 8 + i * 9
        line(d, [cx - cs / 2 - 6, py, cx - cs / 2, py], fill=(64, 220, 150), width=2)
        line(d, [cx + cs / 2, py, cx + cs / 2 + 6, py], fill=(64, 220, 150), width=2)
    for tx, ty in [(86, 20), (86, 48), (120, 34)]:
        line(d, [cx + cs / 2 + 6, cy, x + tx + 60, y + ty], fill=(38, 130, 92), width=1)
        ellipse(d, [x + tx + 57, y + ty - 3, x + tx + 63, y + ty + 3], fill=(64, 220, 150))
    bars = [(196, 16), (222, 26), (248, 38), (274, 54)]
    for bx, bh in bars:
        rect(d, [x + bx, y + h - 8 - bh, x + bx + 18, y + h - 8], fill=(64, 220, 150))


def illo_cyclone(d, x, y, w, h):
    """A spiral storm over a teal sea."""
    rect(d, [x, y, x + w, y + h], fill=(196, 220, 218))
    rect(d, [x, y + h * 0.66, x + w, y + h], fill=TEAL)
    cx, cy = x + w * 0.40, y + h * 0.42
    for r in (30, 22, 15, 8):
        d.arc([u(cx - r), u(cy - r * 0.62), u(cx + r), u(cy + r * 0.62)],
              start=20 + r * 4, end=300 + r * 4, fill=(30, 90, 110), width=u(3))
    ellipse(d, [cx - 4, cy - 3, cx + 4, cy + 3], fill=(30, 90, 110))
    for rx in (216, 244, 268):
        line(d, [x + rx, y + 10, x + rx - 6, y + 24], fill=(90, 130, 150), width=2)
    d.polygon([(u(x + w - 58), u(y + h)), (u(x + w - 30), u(y + h * 0.66)),
               (u(x + w), u(y + h))], fill=SAND)


def illo_nsa(d, x, y, w, h):
    """A columned agency building; one dark screen."""
    rect(d, [x, y, x + w, y + h], fill=NAVY)
    bx, by, bw = x + 26, y + 16, 120
    d.polygon([(u(bx), u(by + 12)), (u(bx + bw / 2), u(by)), (u(bx + bw), u(by + 12))],
              fill=(206, 210, 216))
    rect(d, [bx, by + 14, bx + bw, by + 18], fill=(206, 210, 216))
    for i in range(5):
        rect(d, [bx + 8 + i * 23, by + 20, bx + 15 + i * 23, y + h - 12],
             fill=(206, 210, 216))
    rect(d, [bx - 4, y + h - 12, bx + bw + 4, y + h - 7], fill=(206, 210, 216))
    sx, sy = x + 178, y + 12
    rect(d, [sx, sy, sx + 96, sy + 46], fill=(6, 10, 16), outline=(120, 130, 145))
    ellipse(d, [sx + 44, sy + 19, sx + 52, sy + 27], fill=RED)
    line(d, [sx + 48, sy + 46, sx + 48, sy + 54], fill=(120, 130, 145), width=2)
    line(d, [sx + 36, sy + 56, sx + 60, sy + 56], fill=(120, 130, 145), width=2)


def illo_starship(d, x, y, w, h):
    """A rocket caught by its tower."""
    rect(d, [x, y, x + w, y + h], fill=(206, 220, 230))
    ellipse(d, [x + 14, y + 8, x + 38, y + 32], fill=GOLD)
    tx = x + w - 66
    rect(d, [tx, y + 8, tx + 10, y + h], fill=(90, 96, 104))
    line(d, [tx, y + 26, tx - 30, y + 26], fill=(90, 96, 104), width=4)
    line(d, [tx, y + 38, tx - 30, y + 38], fill=(90, 96, 104), width=4)
    rx = tx - 41
    d.polygon([(u(rx), u(y + 8)), (u(rx + 15), u(y + 8)), (u(rx + 13), u(y + 46)),
               (u(rx + 2), u(y + 46))], fill=(226, 230, 234),
              outline=(90, 96, 104), width=u(1))
    rect(d, [rx + 3, y + 17, rx + 12, y + 24], fill=(90, 96, 104))
    d.polygon([(u(rx + 2), u(y + 46)), (u(rx + 13), u(y + 46)), (u(rx + 7), u(y + 55))],
              fill=(120, 128, 138))
    for i in range(3):
        ellipse(d, [rx - 12 + i * 12, y + h - 18, rx + 10 + i * 12, y + h - 6],
                fill=(240, 242, 244))
    rect(d, [x, y + h - 5, x + w, y + h], fill=(150, 138, 112))


def illo_knesset(d, x, y, w, h):
    """A stone parliament facade."""
    rect(d, [x, y, x + w, y + h], fill=(232, 222, 198))
    bx, by, bw = x + 62, y + 14, 176
    d.polygon([(u(bx), u(by + 12)), (u(bx + bw / 2), u(by)), (u(bx + bw), u(by + 12))],
              fill=(168, 148, 112))
    rect(d, [bx, by + 14, bx + bw, by + 18], fill=(168, 148, 112))
    for i in range(6):
        rect(d, [bx + 10 + i * 28, by + 20, bx + 19 + i * 28, y + h - 12],
             fill=(186, 166, 128))
    rect(d, [bx - 5, y + h - 12, bx + bw + 5, y + h - 7], fill=(168, 148, 112))
    line(d, [x + 30, y + 10, x + 30, y + h - 8], fill=(120, 108, 84), width=2)
    d.polygon([(u(x + 30), u(y + 10)), (u(x + 48), u(y + 15)), (u(x + 30), u(y + 20))],
              fill=(64, 96, 160))


def illo_gaza(d, x, y, w, h):
    """Camp tents and a steaming aid-kitchen pot."""
    rect(d, [x, y, x + w, y + h], fill=(238, 226, 196))
    rect(d, [x, y + h - 12, x + w, y + h], fill=SAND)
    for tx, tw in [(18, 62), (96, 74), (196, 66)]:
        d.polygon([(u(x + tx), u(y + h - 12)), (u(x + tx + tw / 2), u(y + 18)),
                   (u(x + tx + tw), u(y + h - 12))], fill=(206, 196, 172))
        d.polygon([(u(x + tx + tw / 2 - 8), u(y + h - 12)), (u(x + tx + tw / 2), u(y + 34)),
                   (u(x + tx + tw / 2 + 8), u(y + h - 12))], fill=(150, 140, 118))
    px, py = x + w - 52, y + h - 26
    rect(d, [px - 14, py, px + 14, py + 12], fill=(60, 60, 62))
    rect(d, [px - 17, py - 3, px + 17, py], fill=(60, 60, 62))
    for i in range(3):
        d.arc([u(px - 8 + i * 7), u(py - 18), u(px + 2 + i * 7), u(py - 4)],
              start=200, end=330, fill=(150, 150, 148), width=u(2))


# ---------------------------------------------------------------- world map
# Rough continent polygons in (lon, lat); enough for a dotted map.
LAND = [
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-110, 73), (-95, 79),
     (-88, 69), (-82, 73), (-78, 68), (-70, 62), (-64, 60), (-55, 52),
     (-60, 46), (-68, 44), (-73, 40), (-75, 35), (-79, 33), (-80, 27),
     (-83, 30), (-89, 29), (-96, 27), (-97, 22), (-94, 17), (-87, 13),
     (-83, 9), (-79, 9), (-85, 11), (-92, 15), (-102, 18), (-105, 23),
     (-110, 24), (-114, 29), (-120, 34), (-124, 40), (-124, 47),
     (-132, 55), (-150, 60), (-162, 60)],
    [(-78, 7), (-72, 11), (-64, 10), (-55, 6), (-50, 0), (-44, -3),
     (-35, -8), (-40, -20), (-48, -26), (-56, -33), (-62, -39), (-65, -45),
     (-67, -52), (-71, -54), (-73, -46), (-73, -36), (-70, -24), (-70, -18),
     (-75, -15), (-79, -8), (-80, -3), (-78, 2)],
    [(-46, 60), (-42, 63), (-40, 66), (-45, 70), (-52, 71), (-56, 68),
     (-54, 64), (-50, 60)],
    [(-9, 43), (-2, 44), (-1, 46), (-5, 48), (0, 49), (5, 53), (8, 55),
     (8, 57), (18, 56), (21, 59), (24, 58), (28, 59), (30, 60), (28, 66),
     (32, 70), (45, 68), (55, 68), (70, 72), (90, 75), (110, 74),
     (130, 72), (150, 70), (170, 70), (178, 66), (178, 62), (162, 60),
     (158, 52), (150, 45), (142, 42), (140, 38), (135, 35), (129, 33),
     (122, 31), (120, 26), (110, 20), (108, 14), (106, 9), (103, 6),
     (100, 8), (98, 13), (94, 17), (91, 22), (88, 21), (85, 19),
     (80, 15), (77, 8), (73, 16), (70, 21), (66, 25), (61, 25), (57, 26),
     (52, 26), (50, 29), (48, 30), (50, 25), (55, 24), (59, 22), (57, 19),
     (52, 15), (45, 12), (43, 12), (40, 15), (38, 20), (35, 24), (34, 28),
     (36, 33), (30, 36), (27, 37), (23, 36), (19, 40), (15, 38), (12, 42),
     (8, 44), (3, 42), (0, 39), (-2, 37), (-6, 36), (-9, 38)],
    [(-6, 35), (-10, 30), (-15, 25), (-17, 20), (-17, 15), (-12, 8),
     (-8, 5), (2, 6), (6, 4), (9, 4), (13, -1), (12, -8), (14, -18),
     (15, -27), (18, -32), (20, -35), (26, -34), (31, -29), (35, -24),
     (36, -18), (40, -12), (41, -6), (48, -2), (51, 2), (48, 5), (44, 11),
     (40, 15), (39, 20), (37, 24), (34, 27), (33, 30), (30, 31), (22, 33),
     (15, 32), (10, 34), (0, 35)],
    [(113, 22), (114, 14), (118, 6), (120, 2), (117, -2), (113, -4),
     (109, -6), (105, -8), (102, -6), (100, -2), (103, 1), (107, 3),
     (110, 8), (112, 14)],
    [(95, 5), (100, 1), (105, -3), (110, -4), (115, -6), (120, -8),
     (125, -9), (131, -10), (136, -11), (131, -12), (125, -11), (118, -9),
     (110, -7), (102, -4), (97, 2)],
    [(129, -14), (135, -12), (141, -13), (146, -15), (150, -20),
     (153, -26), (150, -33), (147, -38), (141, -38), (135, -35),
     (130, -32), (124, -33), (118, -35), (114, -32), (113, -26),
     (113, -21), (117, -17), (122, -14), (126, -14)],
    [(130, 31), (133, 34), (137, 35), (140, 36), (141, 40), (142, 44),
     (140, 42), (138, 38), (135, 34), (131, 32)],
    [(-5, 50), (-3, 53), (-5, 56), (-8, 55), (-6, 52), (-4, 50)],
    [(167, -45), (172, -41), (174, -38), (176, -38), (173, -41),
     (168, -46), (166, -45)],
    [(44, -13), (47, -15), (49, -18), (48, -22), (46, -25), (44, -23),
     (44, -18), (43, -15)],
]


def in_land(lon, lat):
    for poly in LAND:
        inside = False
        n = len(poly)
        for i in range(n):
            x1, y1 = poly[i]
            x2, y2 = poly[(i + 1) % n]
            if (y1 > lat) != (y2 > lat):
                xin = x1 + (lat - y1) * (x2 - x1) / (y2 - y1)
                if lon < xin:
                    inside = not inside
        if inside:
            return True
    return False


PINS = [  # (number, lon, lat)
    (1, 114, 23), (2, 57, 27), (3, 31, 50), (4, -122, 37), (5, 89, 15),
    (6, -77, 39), (7, -97, 26), (8, 35, 32), (9, 34, 31),
]


def draw_map(d, x, y, w, h):
    cols, rows = 88, 24
    for r in range(rows):
        lat = 80 - r * (138 / (rows - 1))
        for c in range(cols):
            lon = -180 + c * (360 / (cols - 1))
            if in_land(lon, lat):
                px = x + c * (w / (cols - 1))
                py = y + r * (h / (rows - 1))
                ellipse(d, [px - 1.1, py - 1.1, px + 1.1, py + 1.1],
                        fill=(176, 166, 142))
    for num, lon, lat in PINS:
        px = x + (lon + 180) / 360 * w
        py = y + (80 - lat) / 138 * h
        ellipse(d, [px - 7.5, py - 7.5, px + 7.5, py + 7.5], fill=RED)
        f = F(SANS_B, 10)
        s = str(num)
        tw = d.textlength(s, font=f) / S
        text(d, px - tw / 2, py - 6.5, s, f, fill=(255, 252, 244))


# ------------------------------------------------------------------- cards
CARDS = [
    dict(n=1, tag="ASIA · DIPLOMACY", flag="UNDER WAY", illo=illo_shenzhen,
         head="Xi opens APEC as Trump flies in for a three-way summit",
         body="China's president opens the summit in Shenzhen. Trump "
              "arrives from Manila; on Thursday he and Putin sit down "
              "with Xi — a meeting without precedent."),
    dict(n=2, tag="MIDDLE EAST · THE GULF", flag="REPORTED", illo=illo_gulf,
         head="Kuwait and Bahrain intercept Iranian drones",
         body="The interceptions came overnight, aimed across the Gulf. In "
              "Hormuz a gas tanker burns and 21 of its crew are brought "
              "ashore; oil climbs."),
    dict(n=3, tag="EUROPE · WAR IN UKRAINE", flag="REPORTED", illo=illo_ukraine,
         head="UN counts 372 civilians killed in October",
         body="UN monitors put October's civilian toll at 372 killed, as "
              "Russia pounds Kyiv's bridges and Kyiv assesses its "
              "Crimea strike."),
    dict(n=4, tag="BUSINESS · THE CHIP GIANT", flag="REPORTED", illo=illo_nvidia,
         head="Nvidia posts a $115.8 billion quarter",
         body="Revenue of $115.8 billion in one quarter — and the board "
              "rules out bringing founder Jensen Huang back as chief."),
    dict(n=5, tag="ASIA · WEATHER", flag="REPORTED", illo=illo_cyclone,
         head="Cyclone Akvan strengthens in the Bay of Bengal",
         body="The storm is set to turn severe over the bay. Chennai–Yangon "
              "flights are cancelled as coasts on both sides brace."),
    dict(n=6, tag="UNITED STATES · SECURITY", flag="REPORTED", illo=illo_nsa,
         head="The NSA's classified network goes dark",
         body="The spy agency's internal network suffers an outage. Trump "
              "shrugs it off: “like that when you're big and powerful.”"),
    dict(n=7, tag="SPACE · TEXAS", flag="REPORTED", illo=illo_starship,
         head="SpaceX catches a Starship in mid-air",
         body="The giant rocket comes home to Texas and is caught by its "
              "launch tower — the impossible grab, done again."),
    dict(n=8, tag="ISRAEL · POLITICS", flag="REPORTED", illo=illo_knesset,
         head="Knesset elects Kahana as speaker",
         body="Matan Kahana takes the chair with Arab parties' backing, "
              "ousting a Netanyahu ally from the speaker's post."),
    dict(n=9, tag="MIDDLE EAST · GAZA AID", flag="REPORTED", illo=illo_gaza,
         head="One hot meal every two days in Gaza's camps",
         body="In the camps, aid kitchens now serve a single hot meal only "
              "once every two days."),
]

NUMBERS = [
    ("372", "Civilians killed in Ukraine\nin October, UN monitors say"),
    ("$115.8bn", "Nvidia revenue in a single\nquarter, a record for the firm"),
    ("21", "Tanker crew brought ashore\nafter the Hormuz fire"),
    ("19", "Killed as a Russian military\nplane crashes in Siberia"),
]

BRIEFS = [
    (10, "Latvia —", "Parliament backs the Kulbergs government in a confidence vote."),
    (11, "Washington —", "A court sentences Asif Merchant to 27 years over a plot against American officials."),
    (12, "Dhaka —", "India beat Pakistan 2–1 to lift a record 10th SAFF football title."),
    (13, "Turin —", "Zverev is crowned the ATP's year-end No. 1."),
    (14, "Deep sea —", "Rocks that miners want for their metal are found teeming with life."),
    (15, "Siberia —", "A Russian military plane crashes, killing 19."),
]


def draw_brief(d, x, y, w, num, lead, body):
    """A numbered brief: red number, bold place lead, regular text,
    wrapped word by word so the first line flows around the lead."""
    text(d, x, y, str(num), F(SANS_B, 12), fill=RED)
    indent = 22
    words = [(w_, F(SERIF_B, 11.6), INK) for w_ in lead.split()]
    words += [(w_, F(SERIF, 11.6), (52, 50, 46)) for w_ in body.split()]
    cx, cy = x + indent, y
    limit = x + w
    space = d.textlength(" ", font=F(SERIF, 11.6)) / S
    for word, font, fill in words:
        ww = d.textlength(word, font=font) / S
        if cx + ww > limit and cx > x + indent:
            cx = x + indent
            cy += 14.5
        text(d, cx, cy, word, font, fill=fill)
        cx += ww + space


def draw_card(d, x, y, w, h, card):
    rect(d, [x, y, x + w, y + h], fill=CARD, outline=LINE)
    card["illo"](d, x + 10, y + 10, w - 20, 58)
    # tag row
    cy = y + 76
    ellipse(d, [x + 10, cy, x + 27, cy + 17], fill=RED)
    f_num = F(SANS_B, 10.5)
    s = str(card["n"])
    text(d, x + 18.5 - d.textlength(s, font=f_num) / S / 2, cy + 2.2, s,
         f_num, fill=(255, 252, 244))
    tracked(d, x + 34, cy + 2.6, card["tag"], F(SANS_B, 10.5), RED_D, 1.6)
    fw = d.textlength(card["flag"], font=F(SANS_B, 8.5)) / S
    text(d, x + w - 10 - fw, cy + 3.6, card["flag"], F(SANS_B, 8.5), fill=FAINT)
    # headline
    hy = y + 98
    for ln in wrap(d, card["head"], F(SERIF_B, 19.5), w - 20)[:2]:
        text(d, x + 10, hy, ln, F(SERIF_B, 19.5))
        hy += 24
    # summary
    by = hy + 2
    for ln in wrap(d, card["body"], F(SERIF, 12.3), w - 20)[:3]:
        text(d, x + 10, by, ln, F(SERIF, 12.3), fill=(52, 50, 46))
        by += 15.2


def build():
    img = Image.new("RGB", (u(W), u(H)), PAGE)
    d = ImageDraw.Draw(img)
    M = 28
    right = W - M

    # masthead
    tracked(d, M, 22, "THE DAY IN WORLD NEWS", F(SANS_B, 12), NAVY, 3.0)
    tracked(d, 0, 22, "15 STORIES · ONE DAY · ONE PAGE", F(SANS_B, 12),
            RED_D, 3.0, right=right)
    mast = "Wednesday 18 November 2026"
    size = 66
    while d.textlength(mast, font=F(DISPLAY, size)) / S > (right - M):
        size -= 1
    text(d, M, 38, mast, F(DISPLAY, size))
    text(d, M, 110, "A summit opens in Shenzhen, drones fall over the Gulf, "
                    "the UN counts Ukraine's dead — and a starship is caught "
                    "in mid-air.", F(SERIF_I, 15.5), fill=(70, 66, 58))
    line(d, [M, 138, right, 138], fill=INK, width=3)
    line(d, [M, 143, right, 143], fill=INK, width=1)

    # cards, 3 x 3
    cw = (right - M - 28) / 3
    ch = 200
    for i, card in enumerate(CARDS):
        cx = M + (i % 3) * (cw + 14)
        cy = 152 + (i // 3) * (ch + 10)
        draw_card(d, cx, cy, cw, ch, card)

    # by the numbers
    ny = 790
    line(d, [M, ny, right, ny], fill=INK, width=2)
    tracked(d, M, ny + 7, "BY THE NUMBERS", F(SANS_B, 10.5), RED_D, 2.4)
    colw = (right - M) / 4
    for i, (big, label) in enumerate(NUMBERS):
        cx = M + i * colw
        if i:
            line(d, [cx - 12, ny + 28, cx - 12, ny + 54], fill=LINE, width=1)
        text(d, cx, ny + 19, big, F(SERIF_B, 28), fill=NAVY)
        ly = ny + 53
        for ln in label.split("\n"):
            text(d, cx, ly, ln, F(SANS, 10.3), fill=GREY)
            ly += 12.5

    # bottom: map + briefs
    by = 876
    line(d, [M, by - 8, right, by - 8], fill=INK, width=1)
    tracked(d, M, by, "WHERE IT HAPPENED", F(SANS_B, 11), NAVY, 2.2)
    draw_map(d, M, by + 20, 348, 62)
    text(d, M, by + 86, "Numbered dots mark stories 1–9.",
         F(SERIF_I, 10.5), fill=GREY)
    line(d, [396, by, 396, by + 98], fill=LINE, width=1)
    bx = 414
    tracked(d, bx, by, "ALSO ON WEDNESDAY — SIX MORE STORIES",
            F(SANS_B, 11), NAVY, 2.2)
    bw = (right - bx - 18) / 2
    for i, (num, lead, body) in enumerate(BRIEFS):
        cx = bx + (i % 2) * (bw + 18)
        cy = by + 22 + (i // 2) * 31
        draw_brief(d, cx, cy, bw, num, lead, body)

    # footer
    line(d, [M, 986, right, 986], fill=LINE, width=1)
    text(d, M, 992, "Every story was reported on Wednesday 18 November 2026 · "
                    "Sources: Le Monde · Al Jazeera · BBC World · The Guardian · "
                    "UN HRMMU · IMD", F(SANS, 9.3), fill=FAINT)
    tail = "Original drawings"
    tw = d.textlength(tail, font=F(SANS, 9.3)) / S
    text(d, right - tw, 998, tail, F(SANS, 9.3), fill=FAINT)

    img = img.resize((W, H), Image.LANCZOS)
    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
