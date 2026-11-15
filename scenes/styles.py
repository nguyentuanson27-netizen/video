"""Three treatments of the same traveler, terrain, and camera move."""

from random import Random

from PIL import Image, ImageChops, ImageFilter, ImageOps

from scenes.valley import Layer, VIEW, WORLD, valley


STYLES = ("moonlit", "ink-print", "paper-cut")


def tint_warm_shapes(fill, original, tones, dark, light):
    red, green, _, _ = original.split()
    mask = ImageChops.subtract(red, green).point(lambda value: min(255, value * 12))
    accent = ImageOps.colorize(tones, dark, light, blackpoint=25, whitepoint=185)
    fill.paste(accent, (0, 0), mask)


def print_sky(scale):
    sky = Layer(scale)
    sky.gradient((255, 237, 199), (211, 154, 111))
    rng = Random(12)
    sky.ellipse(417, 173, 48, 48, "#ad3829")
    # Uneven ink pickup and fine tooling marks give the print its texture.
    for _ in range(3400):
        x, y = rng.uniform(0, WORLD[0]), rng.uniform(0, 350)
        if (x - 417) ** 2 + (y - 173) ** 2 < 47 ** 2:
            color = rng.choice(["#d76a44", "#c24b35", "#e9a36b"])
        else:
            color = rng.choice(["#d8ab7f", "#edcc9b", "#fceac1"])
        sky.line([(x, y), (x + rng.uniform(.5, 2.1), y + .4)], color)
    for x, y, length in [(92, 114, 163), (566, 127, 65), (774, 92, 174),
                         (170, 190, 112), (522, 215, 109)]:
        for index in range(6):
            strip = length * (1 - index * .10)
            start = x + rng.uniform(-14, 16)
            sky.line([(start, y + index * 4), (start + strip, y + index * 4)],
                     "#e1b383", 1.3)
    return sky.image


def ink_print(layers, scale):
    hatching = Layer(scale)
    for x in range(-WORLD[1], WORLD[0], 7):
        hatching.line([(x, 0), (x + WORLD[1], WORLD[1])], "#ffffff")
    hatch_mask = hatching.image.getchannel("A")
    print_layers = [(layers[0][0], print_sky(scale))]
    inks = [
        ("#694d48", "#dfa583"), ("#352b2e", "#c18056"),
        ("#251d23", "#d48c60"), ("#20191b", "#a96b53"),
    ]
    shading = hatch_mask.point(lambda value: value // 5)
    for (depth, original), (dark, light) in zip(layers[1:], inks):
        alpha = original.getchannel("A")
        tones = ImageOps.grayscale(original)
        print_fill = ImageOps.colorize(tones, dark, light, blackpoint=18, whitepoint=170)
        tint_warm_shapes(print_fill, original, tones, "#902d29", "#eab273")
        contours = tones.filter(ImageFilter.FIND_EDGES).point(lambda value: min(value, 120))
        ink_mask = ImageChops.lighter(contours, shading)
        print_fill.paste(dark, (0, 0, *print_fill.size), ink_mask)
        print_fill.putalpha(alpha)
        print_layers.append((depth, print_fill))
    return print_layers


def paper_sky(scale):
    sky = Layer(scale)
    sky.gradient((104, 152, 147), (231, 219, 168))
    sky.ellipse(420, 177, 49, 49, "#af8067")
    sky.ellipse(417, 173, 49, 49, "#f6c783")
    sky.ellipse(417, 173, 46, 46, "#e88a61")
    for x, y, length in [(70, 163, 180), (725, 114, 178), (514, 230, 73)]:
        points = [(x, y), (x + 38, y - 5), (x + length * .7, y - 5),
                  (x + length, y), (x + length * .78, y + 3), (x + 23, y + 3)]
        sky.polygon([(px + 1, py + 3) for px, py in points], "#86a79a")
        sky.polygon(points, "#b8c7a3")
    return sky.image


def paper_cut(layers, scale):
    paper_layers = [(layers[0][0], paper_sky(scale))]
    swatches = [
        ("#5c8c7c", "#b5c19a", "#ced6aa"),
        ("#367c74", "#a2b090", "#96ae95"),
        ("#1d5755", "#81a888", "#8fba93"),
        ("#183d3e", "#527d69", "#68947b"),
    ]
    shadow_shift = (round(3 * scale), round(6 * scale))
    for (depth, original), (dark, light, rim) in zip(layers[1:], swatches):
        alpha = original.getchannel("A")
        tones = ImageOps.posterize(ImageOps.grayscale(original), 4)
        fill = ImageOps.colorize(tones, dark, light, blackpoint=18, whitepoint=160)
        tint_warm_shapes(fill, original, tones, "#943e31", "#ffc46d")
        edge = Image.new("L", alpha.size)
        edge.paste(alpha, (0, round(2 * scale)))
        bevel = ImageChops.subtract(alpha, edge)
        fill.paste(rim, (0, 0, *fill.size), bevel)
        fill.putalpha(alpha)

        shadow = Image.new("L", alpha.size)
        shadow.paste(alpha, shadow_shift)
        shadow = shadow.filter(ImageFilter.GaussianBlur(3.2 * scale))
        layer = Image.new("RGBA", alpha.size, "#173934")
        layer.putalpha(shadow.point(lambda value: value // 2))
        layer.alpha_composite(fill)
        paper_layers.append((depth, layer))
    return paper_layers


def demo_layers(width, style):
    layers = valley(width)
    scale = width / VIEW[0]
    if style == "ink-print":
        return ink_print(layers, scale)
    if style == "paper-cut":
        return paper_cut(layers, scale)
    return layers
