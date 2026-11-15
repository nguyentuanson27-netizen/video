"""Original illustration for the renderer spike."""

from random import Random

from PIL import Image, ImageDraw


VIEW = (960, 540)
WORLD = (1056, 594)


class Layer:
    def __init__(self, scale):
        self.scale = scale
        self.image = Image.new("RGBA", self.pixels(WORLD))
        self.draw = ImageDraw.Draw(self.image)

    def pixels(self, coordinates):
        return tuple(round(value * self.scale) for value in coordinates)

    def polygon(self, points, color):
        self.draw.polygon([self.pixels(point) for point in points], fill=color)

    def line(self, points, color, width=1):
        self.draw.line(
            [self.pixels(point) for point in points],
            fill=color,
            width=max(1, round(width * self.scale)),
            joint="curve",
        )

    def ellipse(self, x, y, rx, ry, color):
        self.draw.ellipse(self.pixels((x - rx, y - ry, x + rx, y + ry)), fill=color)

    def gradient(self, top, bottom, start=0):
        width, height = self.image.size
        first_row = round(start * self.scale)
        for y in range(first_row, height):
            fraction = (y - first_row) / (height - first_row - 1)
            color = tuple(round(a + (b - a) * fraction) for a, b in zip(top, bottom))
            self.draw.line(((0, y), (width - 1, y)), fill=color)


def pine(layer, x, y, height, color, seed):
    rng = Random(seed)
    layer.polygon([(x - height * .023, y), (x, y - height), (x + height * .017, y)], color)
    for tier in range(9):
        tip = y - height + tier * height * .077
        spread = height * (.050 + tier * .016)
        left, right = spread * rng.uniform(.8, 1.2), spread * rng.uniform(.8, 1.2)
        layer.polygon(
            [(x, tip), (x - left * .56, tip + height * .10),
             (x - left, tip + height * .17), (x - left * .42, tip + height * .15),
             (x - left * .58, tip + height * .19), (x, tip + height * .16),
             (x + right * .72, tip + height * .20), (x + right * .54, tip + height * .15),
             (x + right, tip + height * .18), (x + right * .49, tip + height * .08)],
            color,
        )


def traveler(layer):
    layer.ellipse(704, 424, 43, 7, "#0b1d27")
    layer.polygon([(691, 390), (713, 390), (714, 415), (724, 421), (724, 425),
                   (704, 425), (700, 410), (695, 426), (678, 426), (678, 421),
                   (686, 416)], "#111e2c")
    layer.polygon([(694, 346), (710, 349), (718, 364), (722, 385), (729, 401),
                   (714, 405), (701, 403), (676, 404), (686, 380), (683, 364)], "#ae4939")
    layer.polygon([(707, 350), (720, 366), (723, 390), (730, 401), (712, 406),
                   (702, 400), (706, 382)], "#743333")
    layer.line([(690, 373), (690, 389), (684, 399)], "#d26b4a", 2)
    layer.polygon([(686, 351), (680, 344), (681, 332), (691, 320), (706, 323),
                   (715, 334), (713, 348), (702, 359)], "#9d4337")
    layer.polygon([(687, 335), (684, 341), (678, 344), (684, 346), (686, 352),
                   (694, 350), (696, 337)], "#f3a476")
    layer.line([(685, 332), (691, 324), (704, 324)], "#e17a50", 2)
    layer.polygon([(690, 354), (705, 355), (707, 361), (697, 365), (686, 360),
                   (673, 365), (662, 360), (675, 357)], "#e5a261")
    layer.ellipse(685, 341, 1.2, 1.2, "#40252b")
    layer.line([(693, 366), (679, 382), (664, 379)], "#f08c59", 5)
    layer.ellipse(663, 378, 3, 3, "#f2b785")
    layer.line([(662, 378), (657, 385), (665, 386), (662, 378)], "#d49c5b", 2)
    layer.polygon([(654, 386), (667, 386), (669, 402), (652, 402)], "#884a38")
    layer.polygon([(657, 388), (664, 388), (665, 399), (655, 399)], "#ffbd64")
    layer.ellipse(660, 394, 2.8, 4.5, "#fff1a8")
    layer.line([(650, 402), (671, 402)], "#452830", 3)


def valley(width):
    scale = width / VIEW[0]
    sky, mountains, lake, ridge, reeds = (Layer(scale) for _ in range(5))
    sky.gradient((20, 32, 65), (129, 107, 141))
    moonlight = Layer(scale)
    for radius in range(130, 46, -1):
        opacity = round(62 * ((131 - radius) / 85) ** 2)
        moonlight.ellipse(417, 173, radius, radius, (211, 191, 179, opacity))
    sky.image.alpha_composite(moonlight.image)
    rng = Random(32)
    for _ in range(190):
        x, y = rng.uniform(0, WORLD[0]), rng.uniform(10, 302)
        radius = rng.choice([.3, .45, .55, .8, 1.1])
        sky.ellipse(x, y, radius, radius, rng.choice(["#d8c9c7", "#8f9cb3", "#687893"]))
    for x, y in [(301, 99), (487, 173), (713, 125), (802, 88)]:
        sky.line([(x - 4, y), (x + 4, y)], "#cfbfb5")
        sky.line([(x, y - 4), (x, y + 4)], "#cfbfb5")
    sky.ellipse(417, 173, 47, 47, "#f9deb1")
    sky.ellipse(428, 153, 16, 9, "#f0cda9")
    sky.ellipse(399, 186, 10, 15, "#f4d4ab")
    sky.ellipse(431, 199, 7, 6, "#f1cd9d")

    peaks = [(0, 242), (110, 175), (193, 232), (330, 151), (395, 249),
             (469, 218), (547, 255), (679, 137), (742, 195), (785, 177),
             (883, 241), (970, 166), (1056, 205)]
    mountains.polygon([*peaks, (1056, 370), (0, 370)], "#6f7396")
    for summit, slope, foot in [(peaks[1], (133, 221), (256, 330)),
                                (peaks[3], (342, 229), (433, 330)),
                                (peaks[7], (684, 220), (824, 325)),
                                (peaks[11], (984, 226), (1056, 305))]:
        mountains.polygon([summit, slope, foot, (summit[0] - 123, 349)], "#5e6387")
        mountains.polygon([summit, (summit[0] - 32, summit[1] + 26), slope],
                          "#8d86a1")
    nearer = [(0, 293), (135, 223), (229, 271), (301, 263), (386, 308),
              (546, 282), (608, 313), (753, 230), (854, 257), (971, 231), (1056, 278)]
    mountains.polygon([*nearer, (1056, 367), (0, 367)], "#414f72")
    mountains.polygon([(608, 313), (753, 230), (795, 265), (728, 292),
                       (852, 346), (659, 365)], "#515e80")
    mountains.polygon([(0, 306), (135, 223), (162, 253), (115, 264), (87, 301),
                       (131, 317), (0, 344)], "#4d597b")

    lake.gradient((55, 74, 106), (14, 33, 51), 330)
    for _ in range(190):
        y = rng.uniform(332, 555)
        x = rng.uniform(0, WORLD[0])
        length = rng.uniform(2, 43) * ((y - 275) / 140)
        lake.line([(x, y), (x + length, y)],
                  rng.choice(["#3a526b", "#405574", "#536381", "#344c66"]))
    for _ in range(120):
        y = rng.uniform(333, 470)
        x = rng.gauss(416, 13 + (y - 333) / 3)
        lake.line([(x, y), (x + rng.uniform(2, 22), y)],
                  rng.choice(["#a49da0", "#d3b591", "#74839a", "#8d8897"]))
    for x in range(-8, 1070, 7):
        if 315 < x < 570:
            continue
        y = 331 + 14 * (abs(x - 447) / 610) ** 1.5 + rng.uniform(-3, 4)
        pine(lake, x, y, rng.uniform(6, 31), "#29394d", x)

    ridge.polygon([(0, 517), (149, 523), (310, 503), (478, 465), (613, 437),
                   (694, 420), (762, 423), (849, 402), (954, 414), (1056, 377),
                   (1056, 594), (0, 594)], "#1b3040")
    ridge.polygon([(0, 542), (201, 528), (353, 510), (530, 470), (692, 437),
                   (756, 444), (689, 451), (510, 501), (406, 546), (334, 594),
                   (0, 594)], "#344452")
    ridge.polygon([(567, 458), (688, 430), (745, 430), (702, 440), (620, 455)],
                  "#57616a")
    ridge.polygon([(535, 478), (655, 453), (598, 476), (556, 483)], "#435763")
    for x, y, h in [(104, 530, 112), (207, 523, 80), (856, 416, 98), (930, 421, 127)]:
        pine(ridge, x, y, h, "#223744", x)
    traveler(ridge)

    reeds.polygon([(0, 512), (124, 542), (273, 553), (382, 568), (648, 569),
                   (852, 540), (1056, 509), (1056, 594), (0, 594)], "#101d29")
    for x, y, h in [(15, 570, 380), (72, 556, 290), (997, 566, 366), (1056, 553, 435)]:
        pine(reeds, x, y, h, "#121f2c", x)
    for _ in range(310):
        x = rng.uniform(0, WORLD[0])
        y = 569 - 56 * (abs(x - 530) / 530) ** 2 + rng.uniform(0, 30)
        bend, length = rng.uniform(-11, 11), rng.uniform(5, 32)
        reeds.line([(x, y), (x + bend / 3, y - length * .64),
                    (x + bend, y - length)], rng.choice(["#12222c", "#20363e", "#314950"]))
    return [(0.10, sky.image), (0.30, mountains.image), (0.50, lake.image),
            (0.78, ridge.image), (1.22, reeds.image)]
