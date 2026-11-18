"""Draw the entry image for make.fun news-image-20261118.

A one-page newspaper front page summing up the world news of
Wednesday 18 November 2026, drawn with Pillow primitives (flat
illustration, real fonts, no photographs). Every headline below was
reported on 18 November 2026; the README lists the dated sources.

Run:  python3 make_image.py   ->  writes entry.png beside this file
The shipped entry program (main.py) only copies entry.png; this
generator is kept in the repo so the picture can be redrawn.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024

# ---------------------------------------------------------------- palette
CREAM = (246, 241, 230)
PAPER = (255, 254, 248)
NAVY = (15, 38, 68)
NAVY_D = (10, 26, 48)
GOLD = (198, 156, 74)
RED = (176, 32, 48)
INK = (26, 26, 26)
GREY = (96, 96, 92)
CARD_LINE = (203, 192, 168)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, width):
    """Greedy word wrap to pixel width."""
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


def tracked(draw, xy, text, font, fill, tracking=6, anchor_right=None):
    """Draw letter-spaced text; returns total width drawn."""
    x, y = xy
    total = sum(draw.textlength(ch, font=font) + tracking for ch in text) - tracking
    if anchor_right is not None:
        x = anchor_right - total
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return total


def bands(draw, box, colours):
    """Horizontal gradient made of flat bands."""
    x0, y0, x1, y1 = box
    n = len(colours)
    for i, c in enumerate(colours):
        yy0 = y0 + (y1 - y0) * i // n
        yy1 = y0 + (y1 - y0) * (i + 1) // n
        draw.rectangle([x0, yy0, x1, yy1], fill=c)


# ---------------------------------------------------------------- scenes
def scene_shenzhen(d, box):
    """Dusk skyline of Shenzhen, APEC flags, a plane coming in."""
    x0, y0, x1, y1 = box
    bands(d, box, [(38, 52, 96), (58, 70, 118), (96, 92, 138),
                   (150, 104, 128), (196, 120, 110), (222, 148, 104)])
    d.ellipse([x1 - 118, y0 + 18, x1 - 58, y0 + 78], fill=(246, 196, 110))
    # skyline silhouettes, back row then front row
    back = (30, 40, 74)
    front = (16, 24, 48)
    towers = [(0, 62, 26), (30, 44, 22), (56, 78, 30), (90, 52, 24),
              (118, 96, 34), (156, 58, 26), (186, 84, 30), (220, 48, 22),
              (246, 70, 28), (278, 40, 20), (302, 64, 26), (332, 50, 24),
              (360, 74, 28), (392, 56, 22)]
    base = y1 - 34
    for dx, th, tw in towers:
        d.rectangle([x0 + dx, base - th, x0 + dx + tw, base], fill=back)
    for dx, th, tw in [(8, 40, 30), (70, 60, 34), (150, 46, 30),
                       (232, 66, 36), (318, 44, 30), (382, 58, 32)]:
        d.rectangle([x0 + dx, base - th, x0 + dx + tw, base], fill=front)
        for wy in range(base - th + 7, base - 6, 11):
            for wx in range(x0 + dx + 5, x0 + dx + tw - 5, 9):
                if (wx * 7 + wy * 13) % 5 < 2:
                    d.point((wx, wy), fill=(250, 214, 130))
    # the supertall with its spire
    sx = x0 + 196
    d.polygon([(sx, base), (sx + 13, base - 118), (sx + 26, base)], fill=front)
    d.line([sx + 13, base - 118, sx + 13, base - 132], fill=front, width=3)
    # water and reflections
    d.rectangle([x0, base, x1, y1], fill=(24, 44, 78))
    for i in range(26):
        rx = x0 + (i * 67) % (x1 - x0 - 30)
        ry = base + 5 + (i * 11) % 24
        d.line([rx, ry, rx + 16, ry], fill=(90, 120, 168), width=2)
    # three flags on the shore
    for i, col in enumerate([(206, 44, 54), (52, 92, 168), (236, 236, 232)]):
        fx = x0 + 30 + i * 30
        d.line([fx, base, fx, base - 30], fill=(220, 220, 215), width=2)
        d.polygon([(fx, base - 30), (fx + 15, base - 25), (fx, base - 20)], fill=col)
    # arriving plane, simple side silhouette in the upper left sky
    px, py = x0 + 52, y0 + 22
    ink = (16, 20, 36)
    d.polygon([(px, py + 5), (px + 34, py + 5), (px + 44, py + 9), (px + 34, py + 11),
               (px + 2, py + 11)], fill=ink)                       # fuselage
    d.polygon([(px + 16, py + 8), (px + 26, py + 8), (px + 32, py + 16),
               (px + 24, py + 16)], fill=ink)                       # wing
    d.polygon([(px + 1, py + 5), (px - 5, py - 3), (px + 4, py - 2)], fill=ink)  # tail


def scene_gulf(d, box):
    """A tanker at sea, drones above, smoke on the horizon."""
    x0, y0, x1, y1 = box
    bands(d, box, [(196, 214, 226), (206, 220, 230), (214, 226, 234)])
    d.ellipse([x0 + 18, y0 + 6, x0 + 44, y0 + 32], fill=(244, 200, 105))
    sea = y0 + 34
    d.rectangle([x0, sea, x1, y1], fill=(52, 96, 128))
    for i in range(14):
        rx = x0 + (i * 41) % (x1 - x0 - 24)
        ry = sea + 4 + (i * 7) % (y1 - sea - 6)
        d.line([rx, ry, rx + 13, ry], fill=(120, 165, 195), width=2)
    # tanker
    hx, hy = x0 + 34, sea + 8
    d.polygon([(hx, hy), (hx + 128, hy), (hx + 116, hy + 13), (hx + 10, hy + 13)],
              fill=(38, 42, 50))
    d.rectangle([hx + 16, hy - 9, hx + 108, hy], fill=(150, 60, 48))
    d.rectangle([hx + 96, hy - 20, hx + 110, hy - 9], fill=(226, 224, 216))
    d.rectangle([hx + 100, hy - 26, hx + 106, hy - 20], fill=(90, 90, 90))
    # smoke plume astern, kept inside the scene
    for i, r in enumerate([4, 6, 8, 10]):
        cxp = hx + 14 + i * 6
        cyp = hy - 14 - i * 4
        d.ellipse([cxp - r, cyp - r, cxp + r, cyp + r], fill=(110, 110, 114))
    d.polygon([(hx + 8, hy - 6), (hx + 14, hy - 15), (hx + 20, hy - 6)],
              fill=(238, 128, 44))
    # two drones with dashed paths
    for dx, dy in [(196, 10), (238, 20)]:
        cx, cy = x0 + dx, y0 + dy
        d.line([cx - 9, cy - 6, cx + 9, cy + 6], fill=(30, 30, 34), width=3)
        d.line([cx - 9, cy + 6, cx + 9, cy - 6], fill=(30, 30, 34), width=3)
        for k in range(4):
            d.point((cx - 26 + k * 6, cy + 12 + k * 2), fill=(90, 90, 96))


def scene_ukraine(d, box):
    """A city bridge under a grey sky, smoke rising behind blocks."""
    x0, y0, x1, y1 = box
    bands(d, box, [(168, 172, 178), (178, 182, 186), (188, 190, 192)])
    base = y1 - 16
    for dx, bh, bw in [(6, 26, 30), (42, 34, 26), (74, 22, 34), (150, 30, 28),
                       (214, 24, 32), (252, 32, 26)]:
        d.rectangle([x0 + dx, base - bh, x0 + dx + bw, base], fill=(96, 100, 108))
        for wy in range(base - bh + 5, base - 4, 9):
            for wx in range(x0 + dx + 4, x0 + dx + bw - 4, 8):
                if (wx + wy) % 3 == 0:
                    d.point((wx, wy), fill=(214, 200, 150))
    # smoke column rising behind the blocks
    for i, r in enumerate([5, 7, 9, 11]):
        cxp = x0 + 188 + i * 3
        cyp = y0 + 34 - i * 7
        d.ellipse([cxp - r, cyp - r, cxp + r, cyp + r], fill=(128, 130, 134))
    # bridge deck and two piers over the river strip
    d.rectangle([x0, base, x1, base + 5], fill=(60, 64, 72))
    d.rectangle([x0 + 60, base + 5, x0 + 70, y1], fill=(60, 64, 72))
    d.rectangle([x0 + 216, base + 5, x0 + 226, y1], fill=(60, 64, 72))
    d.rectangle([x0, base + 5, x1, y1], fill=(84, 108, 128))


def scene_chip(d, box):
    """A processor on a dark board, traces running to rising bars."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(14, 34, 30))
    cx, cy, s = x0 + 66, y0 + 29, 40
    for k in range(6):
        px = cx - s // 2 + 6 + k * 7
        d.line([px, cy - s // 2 - 6, px, cy - s // 2], fill=(120, 200, 160), width=2)
        d.line([px, cy + s // 2, px, cy + s // 2 + 6], fill=(120, 200, 160), width=2)
        py = cy - s // 2 + 6 + k * 7
        d.line([cx - s // 2 - 6, py, cx - s // 2, py], fill=(120, 200, 160), width=2)
        d.line([cx + s // 2, py, cx + s // 2 + 6, py], fill=(120, 200, 160), width=2)
    d.rectangle([cx - s // 2, cy - s // 2, cx + s // 2, cy + s // 2],
                fill=(22, 90, 66), outline=(150, 225, 185), width=2)
    d.rectangle([cx - 11, cy - 11, cx + 11, cy + 11], outline=(150, 225, 185), width=2)
    for tx, ty in [(150, 14), (186, 30), (140, 44), (206, 12)]:
        d.line([cx + s // 2 + 6, cy, x0 + tx, y0 + ty], fill=(70, 140, 110), width=2)
        d.ellipse([x0 + tx - 3, y0 + ty - 3, x0 + tx + 3, y0 + ty + 3],
                  fill=(150, 225, 185))
    # rising bars
    for i, bh in enumerate([12, 20, 27, 38]):
        bx = x0 + 226 + i * 17
        d.rectangle([bx, y1 - 8 - bh, bx + 11, y1 - 8], fill=(96, 205, 150))


def scene_cyclone(d, box):
    """A spiral storm over the sea, bearing down on a coast."""
    x0, y0, x1, y1 = box
    bands(d, box, [(52, 104, 128), (62, 116, 138), (74, 128, 148)])
    cx, cy = x0 + 96, y0 + 30
    for r in (34, 26, 18, 10):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=300, end=210,
              fill=(238, 244, 246), width=5)
        d.arc([cx - r, cy - r, cx + r, cy + r], start=120, end=30,
              fill=(214, 230, 236), width=5)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(240, 246, 248))
    # coast on the right with rain streaks
    d.polygon([(x1 - 62, y1), (x1 - 30, y0 + 16), (x1, y0 + 26), (x1, y1)],
              fill=(196, 178, 130))
    for i in range(9):
        rx = x0 + 150 + (i * 13) % 120
        ry = y0 + 6 + (i * 7) % 34
        d.line([rx, ry, rx - 4, ry + 8], fill=(190, 220, 235), width=2)
    for i in range(8):
        rx = x0 + (i * 33) % (x1 - x0 - 20)
        d.line([rx, y1 - 6, rx + 14, y1 - 6], fill=(150, 195, 215), width=2)


def scene_nsa(d, box):
    """A columned agency headquarters at night, screens gone dark."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(12, 20, 40))
    for i in range(22):
        d.point((x0 + (i * 53) % (x1 - x0), y0 + (i * 17) % 20), fill=(200, 210, 235))
    bx, by = x0 + 56, y1 - 12
    d.polygon([(bx, by - 44), (bx + 88, by - 44), (bx + 44, by - 56)], fill=(52, 66, 96))
    for k in range(5):
        px = bx + 8 + k * 18
        d.rectangle([px, by - 42, px + 7, by - 12], fill=(120, 138, 175))
    d.rectangle([bx - 8, by - 12, bx + 96, by], fill=(40, 52, 80))
    # dark window grid beside it: most lights out
    gx, gy = x0 + 176, y0 + 12
    for r in range(4):
        for c in range(6):
            lit = (r * 6 + c) % 7 == 0
            d.rectangle([gx + c * 15, gy + r * 11, gx + c * 15 + 10, gy + r * 11 + 7],
                        fill=(250, 214, 130) if lit else (30, 42, 68))
    # a dish with a broken signal arc
    dx, dy = x0 + 236, y1 - 14
    d.arc([dx - 16, dy - 30, dx + 16, dy + 2], start=200, end=340,
          fill=(150, 165, 200), width=3)
    d.line([dx, dy - 8, dx + 10, dy + 0], fill=(150, 165, 200), width=2)
    d.arc([dx + 2, dy - 44, dx + 26, dy - 20], start=180, end=270,
          fill=(90, 104, 140), width=2)


def scene_starship(d, box):
    """The launch tower catching the returning rocket."""
    x0, y0, x1, y1 = box
    bands(d, box, [(30, 52, 96), (52, 84, 138), (96, 138, 180), (150, 180, 200)])
    tx = x0 + 178
    d.rectangle([tx, y0 + 6, tx + 13, y1 - 6], fill=(40, 46, 58))
    for k in range(5):
        yy = y0 + 12 + k * 10
        d.line([tx, yy, tx + 13, yy + 8], fill=(40, 46, 58), width=2)
        d.line([tx + 13, yy, tx, yy + 8], fill=(40, 46, 58), width=2)
    # chopstick arms reaching left from the tower to grip the rocket
    d.rectangle([tx - 40, y0 + 20, tx, y0 + 26], fill=(40, 46, 58))
    d.rectangle([tx - 40, y0 + 42, tx, y0 + 48], fill=(40, 46, 58))
    # rocket body held between the arms, fins at its base
    rx = tx - 36
    d.rectangle([rx, y0 + 14, rx + 19, y0 + 50], fill=(230, 232, 236))
    d.polygon([(rx, y0 + 14), (rx + 9, y0 + 3), (rx + 19, y0 + 14)], fill=(198, 202, 208))
    d.rectangle([rx, y0 + 42, rx + 19, y0 + 50], fill=(70, 76, 88))
    d.polygon([(rx, y0 + 50), (rx - 5, y0 + 56), (rx + 2, y0 + 56)], fill=(120, 126, 138))
    d.polygon([(rx + 19, y0 + 50), (rx + 24, y0 + 56), (rx + 17, y0 + 56)],
              fill=(120, 126, 138))
    d.polygon([(rx + 4, y0 + 50), (rx + 9, y0 + 60), (rx + 15, y0 + 50)],
              fill=(245, 160, 70))
    # ground smoke and a low sun
    d.ellipse([x0 + 8, y0 + 8, x0 + 34, y0 + 34], fill=(250, 208, 120))
    for i, r in enumerate([10, 15, 20]):
        d.ellipse([x0 + 120 + i * 26 - r, y1 - 14 - r // 2, x0 + 120 + i * 26 + r,
                   y1 - 14 + r // 2], fill=(214, 220, 226))


# ---------------------------------------------------------------- assembly
def card(d, x, y, w, h, accent, scene, kicker, headline, body):
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=CARD_LINE)
    d.rectangle([x, y, x + w, y + 5], fill=accent)
    scene(d, (x + 10, y + 13, x + w - 10, y + 71))
    ty = y + 79
    d.text((x + 12, ty), kicker, font=F(SANS_B, 13), fill=accent)
    ty += 19
    for line in wrap(d, headline, F(SANS_B, 22), w - 24):
        d.text((x + 12, ty), line, font=F(SANS_B, 22), fill=INK)
        ty += 26
    ty += 3
    for line in wrap(d, body, F(SANS, 13), w - 24):
        d.text((x + 12, ty), line, font=F(SANS, 13), fill=INK)
        ty += 17


def strip(d, y, h, header, header_col, text, size=14):
    d.rectangle([28, y, 996, y + h], fill=PAPER, outline=CARD_LINE)
    d.text((40, y + 6), header, font=F(SANS_B, 13), fill=header_col)
    ty = y + 23
    for line in wrap(d, text, F(SANS, size), 944):
        d.text((40, ty), line, font=F(SANS, size), fill=INK)
        ty += size + 3


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 116], fill=NAVY)
    d.rectangle([0, 110, W, 116], fill=NAVY_D)
    tracked(d, (30, 14), "THE WORLD IN ONE DAY", F(SANS_B, 19),
            (196, 205, 224), tracking=7)
    d.text((28, 38), "WEDNESDAY 18 NOVEMBER 2026", font=F(SERIF_B, 47),
           fill=(255, 255, 255))
    d.text((30, 92), "One day. One picture. The news the world woke up to.",
           font=F(SERIF_I, 16), fill=(206, 214, 230))
    d.rectangle([0, 116, W, 121], fill=GOLD)

    # lead story
    lx, ly, lw, lh = 28, 133, 968, 264
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=PAPER, outline=CARD_LINE)
    d.rectangle([lx, ly, lx + lw, ly + 6], fill=RED)
    scene_shenzhen(d, (lx + 16, ly + 22, lx + 442, ly + 200))
    d.text((lx + 16, ly + 206), "Shenzhen, China's tech capital — host of this year's APEC summit",
           font=F(SANS, 13), fill=GREY)
    tx = lx + 462
    d.text((tx, ly + 18), "ASIA  •  APEC SUMMIT OPENS", font=F(SANS_B, 15), fill=RED)
    ty = ly + 42
    for line in wrap(d, "XI HOSTS THE PACIFIC IN SHENZHEN", F(SANS_B, 37), 500):
        d.text((tx, ty), line, font=F(SANS_B, 37), fill=INK)
        ty += 44
    ty += 6
    lead_body = ("China's president opens the APEC summit with a speech and "
                 "a state banquet in Shenzhen. Donald Trump flies in from "
                 "Manila — and on Thursday he and Vladimir Putin sit down "
                 "with Xi: a three-way meeting without precedent.")
    for line in wrap(d, lead_body, F(SANS, 17), 500):
        d.text((tx, ty), line, font=F(SANS, 17), fill=INK)
        ty += 23

    # cards, two rows of three
    cards = [
        (RED, scene_gulf, "MIDDLE EAST  •  THE GULF", "DRONES OVER THE GULF",
         "Kuwait and Bahrain intercept Iranian drones overnight. In Hormuz "
         "a gas tanker burns — 21 of its crew brought ashore. Oil climbs."),
        (NAVY, scene_ukraine, "EUROPE  •  WAR IN UKRAINE", "UN COUNTS OCTOBER'S DEAD",
         "UN monitors count 372 civilians killed in Ukraine in October "
         "alone, as Russia pounds Kyiv's bridges and Kyiv assesses its "
         "Crimea strike."),
        (NAVY, scene_chip, "BUSINESS  •  THE CHIP GIANT", "NVIDIA'S $115.8 BILLION QUARTER",
         "Bumper results — $115.8 billion of revenue in a single quarter — "
         "and the board rules out bringing founder Jensen Huang back as "
         "chief."),
        (RED, scene_cyclone, "ASIA  •  BAY OF BENGAL", "CYCLONE AKVAN BEARS DOWN",
         "Cyclone Akvan strengthens over the Bay of Bengal, set to turn "
         "severe. Chennai–Yangon flights are cancelled as coasts brace."),
        (NAVY, scene_nsa, "UNITED STATES  •  SECURITY", "THE NSA'S NETWORK GOES DARK",
         "The spy agency's classified internal network suffers an outage. "
         "Trump shrugs it off: “like that when you're big and powerful.”"),
        (NAVY, scene_starship, "SPACE  •  TEXAS", "SPACEX CATCHES A STARSHIP",
         "SpaceX's giant rocket comes home to Texas and is caught in "
         "mid-air by its launch tower — the impossible grab, done again."),
    ]
    cw, ch, gap = 310, 208, 19
    for i, (accent, scene, kick, head, body) in enumerate(cards):
        cx = 28 + (i % 3) * (cw + gap)
        cy = 409 + (i // 3) * (ch + 12)
        card(d, cx, cy, cw, ch, accent, scene, kick, head, body)

    strip(d, 849, 70, "ALSO ON 18 NOVEMBER", RED,
          "Israel's Knesset elects Matan Kahana as speaker, ousting a "
          "Netanyahu ally with Arab parties' backing  •  Latvia's parliament "
          "backs the Kulbergs government in a confidence vote  •  In Gaza's "
          "camps, aid kitchens serve one hot meal every two days  •  A U.S. "
          "court sentences Asif Merchant to 27 years over a plot against "
          "American officials", size=13)
    strip(d, 927, 56, "AROUND THE WORLD IN BRIEF", NAVY,
          "India beat Pakistan 2–1 in Dhaka to lift a record 10th SAFF "
          "football title  •  Zverev is crowned the ATP's year-end No. 1 in "
          "Turin  •  Deep-sea rocks that miners want for metal are found "
          "teeming with life  •  A Russian military plane crashes in "
          "Siberia, killing 19")

    d.text((28, 989), "The world news of Wednesday 18 November 2026, as reported that day.",
           font=F(SANS, 12), fill=GREY)
    right = "make.fun  •  news-image-20261118"
    d.text((996 - d.textlength(right, font=F(SANS, 12)), 989), right,
           font=F(SANS, 12), fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
