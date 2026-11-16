"""Draw the four ink-wash keyframes for the pilot storyboard."""

from math import pi, sin
from pathlib import Path
from random import Random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from scenes.styles import curve, fade_into_mist
from scenes.valley import Layer, VIEW
from studio import FPS, WORK, frame_at


SHOT_FRAMES = (0, 326, 684, 970, 1440)
SHOT_NAMES = ("Cuộc thách đấu", "Gió Bắc", "Mặt Trời", "Bàn tay buông áo")
PAPER = (244, 234, 211)
INK = "#34443e"
RUST = "#a64638"


def paper(scale, warmth=0):
    layer = Layer(scale)
    layer.gradient(PAPER, (251, 242 - warmth, 222 - warmth))
    rng = Random(134)
    for _ in range(8400):
        x, y = rng.uniform(0, 1056), rng.uniform(6, 590)
        layer.line([(x, y), (x + rng.uniform(.7, 2.7), y + .3)],
                   rng.choice(["#eadcbf", "#efe3c9", "#f7ebd2", "#f8efd9"]))
    return layer


def ink_ridge(scale, knots, color, end, seed):
    ridge = Layer(scale)
    edge = curve(*knots)
    ridge.polygon([*edge, (knots[-1][0], end + 9), (knots[0][0], end + 9)], color)
    rng = Random(seed)
    for _ in range(2600):
        x, y = rng.uniform(max(0, knots[0][0]), min(1055, knots[-1][0])), rng.uniform(160, end)
        if ridge.image.getpixel(ridge.pixels((x, y)))[3]:
            length = rng.uniform(.5, 7)
            ridge.line([(x, y), (x + length, y - .24 * length)], (198, 180, 145, 75))
    fade_into_mist(ridge, end - 90, end)
    return ridge


def hills(scale, high=False):
    lift = 47 if high else 0
    distant = ink_ridge(
        scale, [(x, y - lift) for x, y in [(-20, 310), (105, 290), (182, 224),
                                                (230, 207), (327, 275), (433, 290),
                                                (548, 266), (601, 203), (690, 232),
                                                (810, 266), (922, 199), (1070, 252)]],
        (104, 108, 83, 100), 387 - lift, 9,
    )
    near = ink_ridge(
        scale, [(x, y - lift) for x, y in [(-20, 326), (90, 324), (242, 360),
                                                (385, 346), (482, 299), (530, 293),
                                                (607, 334), (693, 318), (788, 269),
                                                (841, 275), (937, 328), (1070, 313)]],
        (65, 82, 70, 153), 421 - lift, 26,
    )
    return distant.image.filter(ImageFilter.GaussianBlur(3.7 * scale)), near.image


def water(layer, top, center):
    rng = Random(146)
    for _ in range(360):
        y = rng.uniform(top, 594)
        x = rng.uniform(50, 1050)
        length = rng.uniform(2, 57) * (.42 + .54 * (y - top) / (594 - top))
        layer.line([(x, y), (x + length, y - .35)], (70, 102, 94, rng.randint(16, 56)))
    for _ in range(106):
        y = rng.uniform(top, 580)
        x = rng.gauss(center, 22 + (y - top) * .22)
        layer.line([(x, y), (x + rng.uniform(5, 38), y)], (186, 128, 63, rng.randint(29, 85)))


def bank(layer, edge, color=INK):
    edge = curve(*edge)
    layer.polygon([*edge, (edge[-1][0], 607), (edge[0][0], 607)], color)
    rng = Random(201)
    for _ in range(1100):
        x, y = rng.uniform(0, 1054), rng.uniform(371, 592)
        if layer.image.getpixel(layer.pixels((x, y)))[3]:
            stroke = rng.uniform(.6, 8)
            layer.line([(x, y), (x + stroke, y - stroke * .3)],
                       rng.choice(["#425348", "#556354", "#4c5b4e"]))


def brush_branch(layer, knots, seed):
    points = curve(*knots)
    for index, (a, b) in enumerate(zip(points, points[1:])):
        thickness = 20 * (1 - .92 * index / len(points))
        layer.line([a, b], "#273a35", thickness)
    rng = Random(seed)
    for x, y in knots[1:]:
        for _ in range(135):
            px, py = rng.gauss(x, 37), rng.gauss(y, 8.5)
            layer.line([(px, py), (px + rng.uniform(1, 7), py - 1)],
                       rng.choice([(45, 66, 55, 160), (93, 104, 77, 110), (67, 78, 65, 100)]))


def traveler(layer, x, y, size, pose):
    def world(points):
        return [(x + px * size, y + py * size) for px, py in points]

    def shape(points, tone):
        layer.polygon(world(points), tone)

    def stroke(points, tone, width):
        layer.line(world(points), tone, width * size)

    layer.ellipse(x + 4 * size, y - 1.5 * size, 24 * size, 3.6 * size, "#293d38")
    if pose == "water":
        shape([(-5, -46), (23, -47), (25, -19), (40, -7), (38, -1), (18, -2),
               (8, -19), (-16, -7), (-31, -7), (-30, -14), (-12, -29)], "#303f3b")
        shape(curve((-9, -84), (7, -83), (18, -73), (23, -53), (18, -39),
                    (1, -35), (-24, -42), (-19, -58), (-21, -71)), "#c5b998")
        shape(curve((-15, -89), (-15, -100), (-5, -111), (11, -109),
                    (22, -99), (16, -88), (7, -86)), "#39413b")
        shape([(12, -102), (24, -96), (19, -87), (18, -83), (5, -83), (5, -96)], "#cd9b78")
        stroke(curve((4, -70), (18, -57), (25, -47), (45, -38)), "#a89879", 10)
        stroke([(36, -43), (47, -37), (51, -39)], "#cf9b79", 6)
        return

    if pose == "grip":
        shape([(-15, -44), (10, -44), (18, -8), (31, -5), (30, 0),
               (11, 0), (1, -20), (-11, -2), (-33, -1), (-33, -7)], "#263b35")
        shape(curve((-10, -87), (10, -82), (20, -63), (18, -55), (21, -43),
                    (-5, -43), (-42, -37), (-33, -55), (-29, -74)), RUST)
        stroke(curve((5, -81), (-29, -87), (-47, -74), (-63, -87)), "#b97552", 5)
    else:
        shape([(-13, -45), (11, -42), (21, -18), (37, -6), (37, -1), (23, 0),
               (2, -17), (-12, -28), (-19, -10), (-37, -9), (-34, -16)], "#273b35")
        shape(curve((-13, -88), (4, -85), (17, -71), (16, -55), (21, -39),
                    (2, -34), (-30, -40), (-22, -58), (-26, -73)), RUST)
        stroke(curve((4, -81), (-14, -85), (-23, -76), (-37, -79)), "#b97654", 4)
    shape(curve((-15, -91), (-22, -105), (-14, -119), (2, -122),
                (19, -113), (19, -103), (11, -89), (-4, -84)), "#893f35")
    shape([(10, -114), (19, -110), (25, -104), (19, -101), (18, -94),
           (9, -91), (5, -101)], "#cf9d7c")
    layer.ellipse(x + 15 * size, y - 106 * size, 1.5 * size, 1.3 * size, "#533d36")
    stroke([(-14, -110), (-10, -116), (0, -118)], "#c17b5c", 1.5)
    if pose == "grip":
        stroke(curve((-12, -72), (-2, -57), (15, -63), (18, -77)), "#723a32", 10)
        stroke(curve((10, -70), (23, -62), (22, -71), (13, -78)), "#be7457", 8)
        stroke([(14, -78), (18, -81), (22, -77)], "#d2a180", 5)
        stroke([(12, -75), (16, -78), (19, -73)], "#d9a784", 4)
    else:
        stroke(curve((-15, -73), (-10, -59), (3, -53), (12, -59)), "#773e33", 8)
        stroke([(7, -57), (13, -59)], "#d3a080", 3)
    stroke([(-21, -48), (-12, -56), (-11, -66)], "#b56b50", 1.8)


def contest(scale):
    sky = paper(scale)
    river, land, subject, foreground = (Layer(scale) for _ in range(4))
    sky.ellipse(737, 162, 46, 46, "#bd5a43")
    far, middle = hills(scale)
    water(river, 363, 750)
    bank(land, [(-20, 426), (130, 405), (262, 411), (354, 437), (452, 450),
                (536, 481), (461, 525), (389, 547), (318, 605)])
    land.polygon(curve((-12, 484), (127, 449), (256, 440), (362, 453),
                       (443, 474), (377, 474), (279, 463), (126, 478), (-12, 517)), "#697362")
    traveler(subject, 343, 456, 1.01, "walk")
    brush_branch(foreground, [(-11, 509), (42, 274), (59, 171), (125, 116), (225, 107)], 87)
    brush_branch(foreground, [(42, 274), (86, 216), (152, 180), (223, 166)], 42)
    return [(0.08, sky.image), (0.17, far), (0.31, middle), (0.42, river.image),
            (0.70, land.image), (0.70, subject.image), (1.20, foreground.image)]


def north_wind(scale):
    sky = paper(scale)
    wind, ground, subject, foreground = (Layer(scale) for _ in range(4))
    far, middle = hills(scale, high=True)
    for index, (x, y, length, lift) in enumerate([
        (105, 198, 757, 94), (179, 230, 839, 133), (45, 307, 986, 186),
        (96, 367, 811, 114), (451, 268, 601, 103), (23, 408, 1032, 124),
    ]):
        for trace in range(8):
            x0, y0 = x + trace * 11, y + trace * 3 / 2
            stroke = curve((x0, y0), (x0 + length * .26, y0 - lift * .13),
                           (x + length * .62, y0 - lift * .38), (x + length, y0 - lift))
            for step, section in enumerate(zip(stroke, stroke[1:])):
                envelope = sin(pi * (step + .5) / (len(stroke) - 1))
                opacity = round((82 - trace * 7) * envelope)
                wind.line(section, (66, 87, 78, opacity), 1.4 if index % 3 else 2.2)
    bank(ground, [(-20, 498), (141, 499), (285, 478), (437, 454),
                  (621, 470), (812, 441), (1066, 441)], "#3b4e45")
    traveler(subject, 536, 465, 1.89, "grip")
    rng = Random(282)
    for _ in range(74):
        x, y = rng.uniform(127, 993), rng.uniform(190, 523)
        size = rng.uniform(2, 7)
        if 438 < x < 595 and 223 < y < 469:
            continue
        foreground.polygon([(x, y), (x + size, y - size * .63), (x + 2.1 * size, y - 2),
                            (x + size, y + size * .19)],
                           rng.choice(["#8e805a", "#5a7059", "#a4794e"]))
    return [(0.06, sky.image), (0.15, far), (0.28, middle), (0.45, wind.image),
            (0.76, ground.image), (0.76, subject.image), (1.19, foreground.image)]


def sun(scale):
    sky = paper(scale, 12)
    glow, river, ground, subject, foreground = (Layer(scale) for _ in range(5))
    for radius in range(165, 47, -1):
        opacity = round(105 * (1 - radius / 166) ** 2)
        glow.ellipse(696, 159, radius, radius, (240, 165, 85, opacity))
    sky.image.alpha_composite(glow.image)
    sky.ellipse(696, 159, 49, 49, "#ca6747")
    far, middle = hills(scale)
    water(river, 362, 657)
    for index in range(5):
        x, y = 613 - index * 11, 462 + index * 8
        river.line(curve((x - 22, y), (x + 1, y + 1), (x + 34, y - 2)),
                   (115, 112, 73, 89 - index * 8), 1.7)
    bank(ground, [(359, 601), (437, 520), (550, 495), (666, 471), (785, 441),
                  (911, 412), (1068, 403)], "#405349")
    traveler(subject, 645, 478, 1.39, "water")
    subject.polygon(curve((734, 493), (743, 459), (773, 432), (809, 434),
                          (848, 466), (862, 496), (797, 504)), "#75816b")
    subject.line(curve((744, 462), (770, 445), (795, 441), (824, 449)), "#a3a68b", 4)
    subject.polygon(curve((756, 455), (763, 430), (792, 424), (814, 432), (837, 453),
                          (816, 451), (801, 480), (776, 478), (770, 453)), RUST)
    subject.line(curve((766, 436), (785, 434), (801, 444), (795, 470)), "#d17f56", 4)
    brush_branch(foreground, [(1069, 583), (1020, 339), (1000, 215), (917, 139),
                               (854, 121)], 712)
    return [(0.08, sky.image), (0.17, far), (0.31, middle), (0.48, river.image),
            (0.73, ground.image), (0.73, subject.image), (1.21, foreground.image)]


def release(scale):
    sky = paper(scale, 15)
    river, rock, cloth, hand = (Layer(scale) for _ in range(4))
    far, middle = hills(scale, high=True)
    water(river, 296, 712)
    for index in range(6):
        y = 342 + index * 23
        river.line(curve((650 - 12 * index, y), (733, y + 4), (807 + 7 * index, y - 1)),
                   (176, 115, 63, 107), 1.5)
    bank(rock, [(-8, 577), (135, 564), (241, 515), (417, 483), (540, 480),
                (702, 497), (821, 539), (944, 595)], "#648071")
    cloth.polygon(curve((246, 594), (285, 545), (361, 494), (516, 490), (598, 518),
                        (635, 573), (759, 600)), "#a54b3c")
    cloth.line(curve((319, 590), (384, 539), (477, 513), (515, 527), (522, 565),
                     (573, 597)), "#d28761", 9)
    cloth.line(curve((351, 594), (446, 556), (476, 550), (457, 586)), "#7f4236", 6)
    hand.polygon(curve((-15, 571), (122, 534), (219, 490), (307, 449), (333, 422),
                       (304, 393), (254, 401), (138, 415), (-15, 423)), "#b89f76")
    hand.line(curve((28, 527), (163, 482), (237, 466), (287, 428)), "#d5c49b", 9)
    thumb = [(284, 404), (358, 369), (402, 339), (441, 328), (449, 337), (437, 353), (413, 375)]
    fingers = [(452, 366), (548, 325), (578, 329), (581, 339), (552, 355),
               (493, 385), (574, 355), (605, 353), (613, 364), (590, 382),
               (505, 415), (578, 390), (600, 391), (607, 400), (590, 415),
               (522, 443), (574, 429), (590, 433), (591, 443), (566, 456),
               (496, 480), (423, 482), (349, 456), (300, 445)]
    hand.polygon(curve(*thumb, *fingers), "#c68c6b")
    hand.polygon(curve((316, 414), (385, 390), (445, 376), (481, 392),
                       (510, 419), (480, 452), (426, 462), (370, 446)), "#d89f7a")
    hand.line(curve((375, 437), (407, 419), (445, 411), (473, 416)), "#a96f57", 3)
    hand.line(curve((419, 453), (449, 445), (469, 432)), "#b5795c", 2)
    hand.line(curve((293, 402), (314, 420), (321, 444)), "#82745b", 4)
    return [(0.06, sky.image), (0.14, far), (0.25, middle), (0.41, river.image),
            (0.82, rock.image), (0.82, cloth.image), (1.09, hand.image)]


DRAW_SCENE = (contest, north_wind, sun, release)


def render_board():
    output = WORK / "pilot" / "storyboard"
    output.mkdir(parents=True, exist_ok=True)
    fonts = Path("C:/Windows/Fonts")
    title_font = ImageFont.truetype(fonts / "segoeuib.ttf", 24)
    label_font = ImageFont.truetype(fonts / "segoeui.ttf", 17)
    board = Image.new("RGB", (1200, 756), "#eae0ca")
    labels = ImageDraw.Draw(board)
    labels.text((24, 13), "Gió Bắc và Mặt Trời · Storyboard v1", font=title_font, fill="#273c35")
    width, height = 1280, 720
    scale = width / VIEW[0]
    locked_camera = ((0, 0, 0), (0, 0, 0))
    for index, painter in enumerate(DRAW_SCENE):
        frame = frame_at(painter(scale), width, height, 0, locked_camera)
        frame.save(output / f"s{index + 1:02}.png")
        x, y = 24 + index % 2 * 584, 55 + index // 2 * 349
        start = SHOT_FRAMES[index] / FPS
        stop = SHOT_FRAMES[index + 1] / FPS
        labels.text((x, y), f"{index + 1:02}   {SHOT_NAMES[index]}   ·   {start:.3f}–{stop:.3f} s",
                    font=label_font, fill="#34443e")
        board.paste(frame.resize((568, 319), Image.Resampling.LANCZOS), (x, y + 21))
    board.save(output / "board-v1.png")
    print(output / "board-v1.png")


if __name__ == "__main__":
    render_board()
