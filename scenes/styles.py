"""Three original illustrations of a lantern bearer overlooking a lake."""

from itertools import pairwise
from math import cos, pi, sin
from random import Random

from PIL import Image, ImageChops, ImageFilter, ImageOps

from scenes.valley import Layer, VIEW, WORLD, valley


MOONLIT_CAMERA = ((-30, 7, 0), (39, -4, .035))
CAMERAS = {
    "moonlit": MOONLIT_CAMERA,
    "ink-wash": ((31, -4, .012), (-34, 10, .028)),
    "paper-cut": ((-5, 1, 0), (10, -14, .124)),
}
STYLES = tuple(CAMERAS)


def curve(*knots):
    """Interpolate an open curve through hand-placed control points."""
    padded = (knots[0], *knots, knots[-1])
    points = []
    for index in range(len(knots) - 1):
        before, start, end, after = padded[index:index + 4]
        for step in range(12):
            t = step / 12
            points.append(tuple(
                b + .5 * ((c - a) * t + (2 * a - 5 * b + 4 * c - d) * t**2
                          + (3 * b - 3 * c + d - a) * t**3)
                for a, b, c, d in zip(before, start, end, after)
            ))
    return [*points, knots[-1]]


def fade_into_mist(layer, start, end):
    fade = Image.new("L", layer.image.size)
    y = round(start * layer.scale)
    fade.paste(255, (0, 0, fade.width, y))
    ramp = ImageOps.invert(Image.linear_gradient("L"))
    fade.paste(ramp.resize((fade.width, round((end - start) * layer.scale))), (0, y))
    layer.image.putalpha(ImageChops.multiply(layer.image.getchannel("A"), fade))


def ink_wash(scale):
    paper, mist, rocks, shore, branch = (Layer(scale) for _ in range(5))
    rng = Random(78)
    paper.gradient((240, 232, 211), (250, 242, 224))
    for _ in range(9200):
        x, y = rng.uniform(0, WORLD[0]), rng.uniform(0, WORLD[1])
        paper.line([(x, y), (x + rng.uniform(.7, 2.8), y + .3)],
                   rng.choice(["#e7d9bb", "#eee1c6", "#f4e8cd", "#f7eddb"]))
    paper.ellipse(711, 164, 38, 38, "#bb5745")
    for _ in range(270):
        theta = rng.uniform(0, 2 * pi)
        radius = 36 * rng.random() ** .5
        x, y = 711 + radius * cos(theta), 164 + radius * sin(theta)
        paper.line([(x, y), (x + 1.1, y + .2)], rng.choice(["#c46850", "#cd7862", "#ab4b3d"]))

    distant = curve((196, 379), (263, 352), (326, 329), (410, 311), (471, 240),
                    (512, 249), (552, 301), (632, 322), (696, 305),
                    (767, 227), (792, 243), (841, 300), (950, 306), (1060, 272))
    mist.polygon([*distant, (1060, 394), (196, 394)], (96, 102, 91, 83))
    fade_into_mist(mist, 316, 382)

    hill = curve((452, 391), (504, 373), (604, 345), (651, 301), (689, 275),
                 (728, 263), (749, 288), (764, 307), (807, 301), (836, 328),
                 (899, 336), (970, 284), (1023, 277), (1061, 309))
    rocks.polygon([*hill, (1061, 406), (452, 406)], (52, 64, 60, 170))
    for _ in range(1450):
        x, y = rng.uniform(610, 1060), rng.uniform(264, 398)
        px, py = rocks.pixels((x, y))
        if px < rocks.image.width and rocks.image.getpixel((px, py))[3]:
            length = min(rng.uniform(1, 7), (1026 - x) / 4 + 12)
            rocks.line([(x, y), (x + length, y + length * .37)],
                       rng.choice([(43, 55, 50, 174), (102, 111, 98, 145),
                                   (154, 153, 133, 104)]))
    fade_into_mist(rocks, 318, 395)
    for _ in range(140):
        y = rng.uniform(342, 526)
        x = rng.uniform(353, WORLD[0])
        length = rng.uniform(3, 50)
        rocks.line([(x, y), (x + length, y - .25)], (87, 106, 96, rng.randrange(12, 55)))

    bank = curve((-15, 391), (75, 385), (142, 383), (212, 405), (305, 417),
                 (368, 444), (314, 460), (276, 482), (181, 537), (116, 594))
    shore.polygon([*bank, (-15, 600)], "#35443f")
    shore.polygon([*curve((-12, 435), (92, 414), (181, 415), (274, 432),
                          (339, 448), (292, 457), (214, 452), (111, 490), (-12, 503))],
                  "#5e6a5c")
    for _ in range(920):
        x, y = rng.uniform(0, 363), rng.uniform(383, 591)
        if shore.image.getpixel(shore.pixels((x, y)))[3]:
            shore.line([(x, y), (x + rng.uniform(1, 8), y - rng.uniform(.2, 3))],
                       rng.choice(["#46534a", "#627062", "#38463e"]))
    shore.ellipse(282, 421, 35, 4, "#34453e")
    shore.polygon([(274, 381), (293, 380), (297, 416), (306, 420),
                   (287, 421), (283, 398), (275, 422), (260, 422)], "#222d2b")
    shore.polygon(curve((279, 333), (293, 335), (303, 353), (303, 375),
                        (315, 397), (293, 391), (259, 398), (268, 372), (268, 351)),
                  "#a7493d")
    shore.polygon(curve((275, 331), (274, 315), (286, 305), (303, 316),
                        (297, 330), (285, 344)), "#8d3d33")
    shore.polygon([(294, 317), (306, 324), (299, 329), (297, 334), (286, 337),
                   (289, 324)], "#d8a189")
    shore.line(curve((301, 339), (283, 338), (268, 346), (249, 340)), "#c07659", 4)
    shore.line(curve((291, 346), (304, 361), (322, 354)), "#793b32", 6)
    shore.line([(322, 354), (323, 365)], "#39423a", 2)
    shore.polygon([(318, 363), (329, 363), (331, 380), (316, 380)], "#876038")
    shore.polygon([(320, 365), (327, 365), (328, 377), (318, 377)], "#f7cc80")

    for knots, width in [
        (((1, 595), (38, 365), (64, 217), (36, 73), (11, -15)), 26),
        (((45, 327), (91, 211), (139, 154), (219, 117), (274, 124)), 11),
        (((61, 223), (85, 117), (147, 49), (235, 30)), 9),
        (((122, 176), (185, 167), (260, 184), (320, 167)), 5),
        (((89, 110), (88, 62), (67, 27)), 6),
    ]:
        stroke = curve(*knots)
        for index, endpoints in enumerate(pairwise(stroke)):
            weight = width * (1 - .89 * index / (len(stroke) - 1))
            branch.line(endpoints, "#263733", weight)
    for center_x, center_y, spread in [(113, 52, 57), (229, 111, 51), (296, 164, 32),
                                        (48, 131, 36), (179, 153, 47), (211, 30, 42)]:
        for _ in range(240):
            x, y = rng.gauss(center_x, spread * .55), rng.gauss(center_y, spread * .19)
            branch.line([(x, y), (x + rng.uniform(1, 6), y - 1)],
                        rng.choice([(35, 52, 47, 220), (45, 65, 56, 176), (68, 83, 69, 133)]),
                        rng.uniform(.55, 2.2))
    return [(0.08, paper.image), (0.20, mist.image.filter(ImageFilter.GaussianBlur(4 * scale))),
            (0.35, rocks.image), (0.72, shore.image), (1.28, branch.image)]


def cardstock(layer, color):
    """Add the offset edge and soft shadow of the sheet under each cutout."""
    fill = layer.image
    alpha = fill.getchannel("A")
    offset = round(7 * layer.scale)
    cast = Image.new("L", alpha.size)
    cast.paste(alpha, (offset, offset * 2))
    sheet = Image.new("RGBA", alpha.size, "#2d243e")
    sheet.putalpha(cast.filter(ImageFilter.GaussianBlur(offset)).point(lambda a: a * 2 // 5))
    edge = Image.new("L", alpha.size)
    edge.paste(alpha, (round(offset / 3), offset))
    base = Image.new("RGBA", alpha.size, color)
    base.putalpha(edge)
    sheet.alpha_composite(base)
    sheet.alpha_composite(fill)
    return sheet


def cut_wave(layer, waterline, height, period, color):
    crest = [(x, waterline + height * sin(2 * pi * x / period))
             for x in range(-12, WORLD[0] + 21, 4)]
    layer.polygon([*crest, (1068, 606), (-12, 606)], color)
    layer.line(crest, "#b2e2d7", 1.3)


def paper_cut(scale):
    board, hills, water, bank, bridge, reeds = (Layer(scale) for _ in range(6))
    rng = Random(24)
    board.gradient((241, 195, 175), (253, 220, 181))
    moon = Layer(scale)
    moon.ellipse(534, 179, 94, 94, "#f8b24f")
    moon.ellipse(534, 179, 89, 89, "#ffce6c")
    moon.ellipse(523, 161, 68, 61, "#ffda83")
    board.image.alpha_composite(cardstock(moon, "#da834c"))
    for origin_x, origin_y, length in [(154, 157, 184), (724, 143, 214), (827, 234, 114)]:
        cloud = curve((origin_x, origin_y), (origin_x + length * .22, origin_y - 7),
                      (origin_x + length * .44, origin_y - 7),
                      (origin_x + length * .54, origin_y - 18),
                      (origin_x + length * .72, origin_y - 15),
                      (origin_x + length, origin_y), (origin_x + length * .83, origin_y + 5),
                      (origin_x + length * .22, origin_y + 5))
        board.polygon([(x + 3, y + 6) for x, y in cloud], "#e6a48e")
        board.polygon(cloud, "#ffe6bd")
    for _ in range(7500):
        x, y = rng.uniform(0, WORLD[0]), rng.uniform(0, WORLD[1])
        board.line([(x, y), (x + 1, y)], (248, 228, 196, 255))

    crest = curve((-12, 263), (104, 219), (221, 218), (300, 281), (391, 295),
                  (491, 351), (564, 351), (652, 285), (736, 301), (838, 214),
                  (947, 216), (1068, 264))
    hills.polygon([*crest, (1068, 434), (-12, 434)], "#aa7499")
    hills.line(crest, "#e8bdc4", 2.5)
    fold = curve((-12, 300), (120, 273), (232, 282), (328, 332),
                 (438, 353), (577, 379), (720, 343), (884, 291), (1068, 268))
    hills.polygon([*fold, (1068, 439), (-12, 439)], "#765783")
    hills.line(fold, "#ba8da8", 2)

    cut_wave(water, 380, 15, 195, "#3c9491")
    cut_wave(water, 423, 15, 230, "#66bbb2")
    cut_wave(water, 466, 17, 244, "#399990")
    cut_wave(water, 519, 19, 275, "#257374")
    for x, y, length in [(105, 403, 77), (801, 407, 79), (395, 450, 88),
                          (662, 478, 71), (230, 495, 83), (805, 531, 94),
                          (37, 518, 114), (591, 545, 63)]:
        water.line(curve((x, y), (x + length * .4, y - 4), (x + length, y)),
                   "#a7dbca", 2.5)

    left_bank = curve((-12, 421), (106, 433), (190, 457), (281, 492), (326, 539), (281, 608))
    right_bank = curve((1068, 390), (956, 420), (878, 465), (817, 500), (793, 607))
    bank.polygon([*left_bank, (-12, 608)], "#423f68")
    bank.polygon([*right_bank, (1068, 608)], "#423f68")
    bank.line(left_bank, "#9a7497", 3)
    bank.line(right_bank, "#9a7497", 3)

    arch_top = curve((235, 514), (368, 452), (451, 405), (531, 394),
                     (624, 409), (711, 456), (847, 510))
    arch_bottom = curve((847, 526), (716, 491), (636, 450), (529, 432),
                        (434, 449), (333, 492), (235, 530))
    bridge.polygon([*arch_top, *arch_bottom], "#e9ac68")
    bridge.line(arch_top, "#ffe0a4", 4)
    for x, y, tilt in [(350, 463, 8), (393, 439, 13), (443, 416, 11),
                        (494, 402, 5), (547, 400, 0), (602, 408, -6),
                        (651, 425, -12), (702, 454, -10), (744, 477, -9)]:
        bridge.line([(x, y), (x + tilt, y + 26)], "#b07869", 2)

    bridge.ellipse(539, 395, 49, 5, "#c28562")
    bridge.polygon([(521, 367), (551, 366), (562, 393), (545, 396),
                    (538, 381), (528, 396), (509, 396)], "#333455")
    cloak = curve((533, 318), (551, 326), (557, 347), (575, 371),
                  (549, 381), (511, 378), (499, 370), (516, 348), (521, 328))
    bridge.polygon([(x + 3, y + 6) for x, y in cloak], "#853f60")
    bridge.polygon(cloak, "#ce535d")
    bridge.polygon(curve((529, 322), (519, 309), (526, 291), (544, 286),
                         (563, 299), (564, 312), (550, 322)), "#b3485a")
    bridge.ellipse(549, 308, 11, 13, "#ffd097")
    bridge.ellipse(555, 307, 1.6, 1.6, "#57364e")
    bridge.line(curve((550, 324), (533, 323), (517, 329), (500, 322)), "#f4bb66", 6)
    bridge.line(curve((545, 338), (559, 351), (578, 339)), "#9b4661", 8)
    bridge.ellipse(579, 338, 4, 4, "#ffc890")
    bridge.line([(579, 340), (584, 349), (574, 349), (579, 340)], "#5e4664", 2.5)
    bridge.polygon([(572, 349), (587, 349), (589, 369), (569, 369)], "#704b62")
    bridge.polygon([(575, 352), (584, 352), (585, 366), (573, 366)], "#ffdc73")

    for x, y, reach, bend, color in [
        (50, 602, 365, 8, "#3b345a"), (89, 602, 253, 87, "#66517b"),
        (161, 608, 174, 106, "#bd777c"), (1011, 600, 434, -38, "#45365c"),
        (994, 605, 320, -119, "#724b76"), (924, 606, 206, -126, "#b46b80"),
    ]:
        stem = curve((x, y), (x + bend * .28, y - reach * .35), (x + bend, y - reach))
        reeds.line(stem, color, 6)
        for index, (leaf_x, leaf_y) in enumerate(stem[4:-1:3]):
            sign = (-1) ** index
            size = 22 + reach * .11 - index * 4
            tip = (leaf_x + sign * size, leaf_y - size * .73)
            leaf = curve((leaf_x, leaf_y), (leaf_x + sign * size * .13, leaf_y - size * .75),
                         tip, (leaf_x + sign * size * .68, leaf_y - size * .20))
            reeds.polygon(leaf, color)
            reeds.line([(leaf_x, leaf_y), tip], "#c1919a", 1)
    return [(0.06, board.image), (0.18, cardstock(hills, "#674d7b")),
            (0.35, cardstock(water, "#277470")), (0.56, cardstock(bank, "#2e2a4e")),
            (0.73, cardstock(bridge, "#996475")), (1.22, cardstock(reeds, "#32243e"))]


def demo_layers(width, style):
    scale = width / VIEW[0]
    if style == "ink-wash":
        return ink_wash(scale)
    if style == "paper-cut":
        return paper_cut(scale)
    return valley(width)
