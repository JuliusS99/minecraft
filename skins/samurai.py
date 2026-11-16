"""Samurai skin, 64x64, classic (4px arms). Run: python3 skins/samurai.py"""
import random
from pathlib import Path
from PIL import Image

random.seed(7)
OUT = Path(__file__).parent

P = {
    'K': (28, 28, 34), 'k': (56, 56, 66), 'H': (18, 16, 20),          # lacquer / hair
    'S': (222, 170, 126), 's': (190, 136, 96), 'b': (30, 20, 16),     # skin, brows
    'W': (236, 234, 226), 'E': (20, 20, 24),                          # white, pupil
    'R': (168, 26, 34), 'L': (210, 60, 60), 'd': (100, 14, 22),       # armor red
    'G': (232, 184, 62), 'g': (170, 124, 34),                         # gold lacing
    'P': (42, 46, 76), 'p': (28, 30, 52),                             # hakama indigo
    'Y': (176, 140, 82),                                              # straw sole
}


def faces(ox, oy, w, h, d):
    return {'top': (ox + d, oy, w, d), 'bottom': (ox + d + w, oy, w, d),
            'right': (ox, oy + d, d, h), 'front': (ox + d, oy + d, w, h),
            'left': (ox + d + w, oy + d, d, h), 'back': (ox + 2 * d + w, oy + d, w, h)}


def paint(img, rect, rows):
    x, y, w, h = rect
    assert len(rows) == h and all(len(r) == w for r in rows), (rect, rows)
    for j, row in enumerate(rows):
        for i, c in enumerate(row):
            if c == '.':
                continue
            n = random.randint(-6, 6)  # subtle texture noise
            img.putpixel((x + i, y + j), tuple(max(0, min(255, v + n)) for v in P[c]) + (255,))


def part(img, ox, oy, w, h, d, spec):
    f = faces(ox, oy, w, h, d)
    for name, rows in spec.items():
        paint(img, f[name], rows)


mirror = lambda rows: [r[::-1] for r in rows]
blank = lambda w, h: ['.' * w] * h

img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))

# --- Head ---------------------------------------------------------------
head_side = ["HHHHHHHH", "HHHHHSSS", "HHHHSSSS", "HHHHSsSS",
             "HHHSSSSS", "HHHSSSSS", "HHSSSSSS", "HHSSSSSS"]
part(img, 0, 0, 8, 8, 8, {
    'front': ["HHHHHHHH", "HSSSSSSH", "SbbSSbbS", "SWESSEWS",
              "SSSssSSS", "SSbbbbSS", "SSSddSSS", "SSSSSSSS"],
    'right': head_side, 'left': mirror(head_side),
    'back': ["HHHHHHHH"] * 8, 'top': ["HHHHHHHH"] * 8, 'bottom': ["ssssssss"] * 8,
})
# Kabuto helmet with gold crescent crest + red menpo face mask
helm_side = ["KKKKKKKK", "GGGGGGGG", "RRRRRR..", "ddgddd..",
             "RRRRR...", "ddgdd...", "GGGG....", "........"]
part(img, 32, 0, 8, 8, 8, {
    'front': ["GKKGGKKG", "KGGGGGGK", "K......K", "K......K",
              "RR....RR", "RRHHHHRR", "RHWWWWHR", "RRRHHRRR"],
    'right': helm_side, 'left': mirror(helm_side),
    'back': ["KKKKKKKK", "GGGGGGGG", "RRRRRRRR", "ddgddgdd",
             "RRRRRRRR", "ddgddgdd", "GGGGGGGG", "........"],
    'top': ["KkKkkKkK"] * 3 + ["KkKGGkKk"] * 2 + ["KkKkkKkK"] * 3,
    'bottom': blank(8, 8),
})

# --- Body: lacquered do armor, gold mon, obi, kusazuri --------------------
front = ["KKWSSWKK", "LKKWWKKL", "RRRGGRRR", "RRGRRGRR", "RRRGGRRR", "ddgddgdd",
         "RRRRRRRR", "ddgddgdd", "KKKGGKKK", "RRdRRdRR", "RRdRRdRR", "GGdGGdGG"]
back = ["KKKKKKKK", "LLLLLLLL", "RRRRRRRR", "ddgddgdd", "RRRRRRRR", "ddgddgdd",
        "RRRRRRRR", "ddgddgdd", "KKKKKKKK", "RRdRRdRR", "RRdRRdRR", "GGdGGdGG"]
side = ["KKKK", "LLLL", "RRRR", "dgdd", "RRRR", "dgdd",
        "RRRR", "dgdd", "KKKK", "RdRR", "RdRR", "GdGG"]
part(img, 16, 16, 8, 12, 4, {
    'front': front, 'back': back, 'right': side, 'left': mirror(side),
    'top': ["KKKKKKKK", "KKKKKKKK", "KKWWWWKK", "KKWSSWKK"], 'bottom': ["pppppppp"] * 4,
})
# Jacket layer: armor shell (obi stays inset) + katana on the back
shell = lambda rows: ['.' * len(rows[0]) if i in (0, 1, 8) else r for i, r in enumerate(rows)]
katana = []
for r in range(12):
    row = ['.'] * 8
    x = r // 2  # ponytail: 1:2 diagonal, handle top-left -> tip bottom-right
    if r < 4:
        row[x], row[x + 1] = ('W', 'K') if r % 2 == 0 else ('K', 'W')  # tsuka wrap
    elif r == 4:
        for i in range(x - 1, x + 3):
            row[i] = 'G'  # tsuba
    elif r < 11:
        row[x], row[x + 1] = 'k', 'H'  # saya
    else:
        row[x], row[x + 1] = 'G', 'G'  # kojiri
    katana.append(''.join(row))
part(img, 16, 32, 8, 12, 4, {
    'front': shell(front), 'back': katana, 'right': shell(side), 'left': shell(mirror(side)),
    'top': blank(8, 4), 'bottom': blank(8, 4),
})

# --- Arms: indigo sleeves, gold cuff, chain kote, sode shoulder plates ------
arm = ["PPPP", "PPPP", "PPPP", "PPPP", "PpPP", "PPpP", "PPPP",
       "GGGG", "KkKk", "kKkK", "KkKk", "SSSS"]
sode = ["LLLL", "dgdd", "RRRR", "dgdd", "GGGG"] + ["...."] * 7
for (bx, by), (ox, oy) in (((40, 16), (40, 32)), ((32, 48), (48, 48))):
    part(img, bx, by, 4, 12, 4, {k: arm for k in ('front', 'back', 'right', 'left')}
         | {'top': ["PPPP"] * 4, 'bottom': ["SSSS"] * 4})
    part(img, ox, oy, 4, 12, 4, {k: sode for k in ('front', 'back', 'right', 'left')}
         | {'top': ["RRRR", "RLLR", "RLLR", "RRRR"], 'bottom': blank(4, 4)})

# --- Legs: pleated hakama, suneate shin guards, tabi + straw sandals --------
leg = ["PPPP", "PpPP", "PpPP", "PpPP", "PpPp", "PpPp", "PPPp",
       "GGGG", "KkKK", "KkKK", "KkKK", "WWWW"]
leg_back = ["PPPP", "PPpP", "PPpP", "PPpP", "pPpP", "pPpP", "pPPP",
            "PPPP", "pPPp", "pPPp", "pPPp", "WWWW"]
guard = ["...."] * 7 + ["GGGG", "KkKK", "KkKK", "KkKK", "...."]
for (bx, by), (ox, oy), flip in (((0, 16), (0, 32), False), ((16, 48), (0, 48), True)):
    m = mirror if flip else (lambda r: r)
    part(img, bx, by, 4, 12, 4, {'front': m(leg), 'right': leg, 'left': mirror(leg),
                                 'back': m(leg_back), 'top': ["PPPP"] * 4, 'bottom': ["YYYY"] * 4})
    part(img, ox, oy, 4, 12, 4, {'front': m(guard), 'right': guard, 'left': mirror(guard),
                                 'back': blank(4, 12), 'top': blank(4, 4), 'bottom': blank(4, 4)})

img.save(OUT / 'samurai.png')

# --- Preview: front + back, overlays on top, 12x ----------------------------
def view(parts):
    v = Image.new('RGBA', (16, 32), (0, 0, 0, 0))
    for base, over, at in parts:
        for rect in (base, over):
            x, y, w, h = rect
            tile = img.crop((x, y, x + w, y + h))
            v.alpha_composite(tile, at)
    return v

front_v = view([((8, 8, 8, 8), (40, 8, 8, 8), (4, 0)), ((20, 20, 8, 12), (20, 36, 8, 12), (4, 8)),
                ((44, 20, 4, 12), (44, 36, 4, 12), (0, 8)), ((36, 52, 4, 12), (52, 52, 4, 12), (12, 8)),
                ((4, 20, 4, 12), (4, 36, 4, 12), (4, 20)), ((20, 52, 4, 12), (4, 52, 4, 12), (8, 20))])
back_v = view([((24, 8, 8, 8), (56, 8, 8, 8), (4, 0)), ((32, 20, 8, 12), (32, 36, 8, 12), (4, 8)),
               ((44, 52, 4, 12), (60, 52, 4, 12), (0, 8)), ((52, 20, 4, 12), (52, 36, 4, 12), (12, 8)),
               ((28, 52, 4, 12), (12, 52, 4, 12), (4, 20)), ((12, 20, 4, 12), (12, 36, 4, 12), (8, 20))])
S = 12
prev = Image.new('RGBA', (16 * S * 2 + 3 * S * 2, 32 * S + 2 * S * 2), (70, 80, 95, 255))
prev.alpha_composite(front_v.resize((16 * S, 32 * S), Image.NEAREST), (2 * S, 2 * S))
prev.alpha_composite(back_v.resize((16 * S, 32 * S), Image.NEAREST), (20 * S, 2 * S))
prev.save(OUT / 'samurai_preview.png')

assert img.size == (64, 64) and img.getpixel((12, 11))[3] == 255  # face painted
print('ok')
