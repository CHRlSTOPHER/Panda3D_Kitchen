from enum import Enum


class ToonColors(Enum):
    # Classic Toon Colors
    PEACH = (0.969, 0.69, 0.698)
    BRIGHT_RED = (0.933, 0.263, 0.278)
    RED = (0.863, 0.404, 0.416)
    MAROON = (0.71, 0.231, 0.435)
    SIENNA = (0.569, 0.447, 0.161)
    BROWN = (0.639, 0.353, 0.267)
    TAN = (0.996, 0.694, 0.51)
    CORAL = (0.831, 0.502, 0.294)
    ORANGE = (0.992, 0.478, 0.165)
    YELLOW = (0.996, 0.898, 0.318)
    CREAM = (0.996, 0.957, 0.596)
    CITRINE = (0.855, 0.933, 0.49)
    LIME = (0.549, 0.824, 0.322)
    SEA_GREEN = (0.239, 0.741, 0.514)
    GREEN = (0.302, 0.969, 0.4)
    LIGHT_BLUE = (0.431, 0.906, 0.835)
    AQUA = (0.345, 0.82, 0.953)
    BLUE = (0.188, 0.561, 0.773)
    PERIWINKLE = (0.557, 0.588, 0.875)
    ROYAL_BLUE = (0.282, 0.325, 0.725)
    SLATE_BLUE = (0.459, 0.376, 0.824)
    PURPLE = (0.545, 0.278, 0.749)
    LAVENDER = (0.725, 0.471, 0.859)
    PINK = (0.898, 0.616, 0.906)

    # Fan Additions
    ROSE_PINK = (0.89, 0.439, 0.698)
    ICE_BLUE = (0.741, 0.875, 0.957)
    MINT_GREEN = (0.639, 0.859, 0.675)
    EMERALD = (0.039, 0.863, 0.655)
    TEAL = (0.196, 0.725, 0.714)
    APRICOT = (0.984, 0.537, 0.396)
    AMBER = (0.969, 0.749, 0.349)
    CRIMSON = (0.659, 0.176, 0.259)
    DARK_GREEN = (0.412, 0.643, 0.282)
    STEEL_BLUE = (0.325, 0.408, 0.6)
    BEIGE = (0.804, 0.757, 0.612)
    BUBBLEGUM = (0.996, 0.357, 0.447)
    CARTOONIVAL_BLUE = (0.227, 0.58, 0.98)
    CARTOONIVAL_PINK = (0.933, 0.369, 0.82)
    SPOOKY_PURPLE = (0.357, 0.239, 0.502)
    SPOOKY_GREEN = (0.678, 1, 0.361)
    BLACK = (0.298, 0.298, 0.353)
    WHITE = (1.0, 1.0, 1.0)


'''
Here's a visual reference for the colors:
https://toontownrewritten.fandom.com/wiki/Toon_colors
No internet? Call the print_toon_colors function in here and run this py file!
'''
def print_toon_colors():
    ANSI_text = "\33[38;2;{red};{green};{blue}m{name}"
    color_names = [color for color in ToonColors]
    for name in color_names:
        red = int(name.value[0] * 255)
        green = int(name.value[1] * 255)
        blue = int(name.value[2] * 255)
        color_text = ANSI_text.format(red=red, green=green, blue=blue,
                                      name=str(name)[11:])
        print(color_text)

# print_toon_colors()