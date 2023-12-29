from classes.globals import Globals as G

FRAME_TEXTURE = G.APP_MAPS + "mat_panel"
LASHES_TEXTURE = G.APP_MAPS + "lashes-buttons" + G.PNG
BOTTOMS_TEXTURE = G.APP_MAPS + "bottoms-buttons" + G.PNG
SPECIES_TEXTURE = G.APP_MAPS + "toon-species-buttons" + G.JPG
GXZ = .165
GENDER_POS = [(-GXZ, 0, GXZ), (GXZ, 0, GXZ), (-GXZ, 0, -GXZ), (GXZ, 0, -GXZ)]
BOTTOM_DICT = {'m': "shorts", "f": "skirt"}
BODY_SIZES = ['ss', 'sm', 'sl', 'ms', 'mm', 'ml', 'ls', 'lm', 'll']
BODY_POS = [
    (-.75, 0, .4), (-.45, 0, .4), (-.15, 0, .4),
    (-.75, 0, -.05), (-.45, 0, -.05), (-.15, 0, -.05),
    (.15, 0, -.05), (.45, 0, -.05), (.75, 0, -.05)
]
HEAD_DISPLAYS = ['ss', 'ls', 'sl', 'll']
HEAD_POS = [
    (.35, 0, .71),
    (.15, 0, .5),
    (.75, 0, .71),
    (.525, 0, .5),
]
MOUSE_HEAD_POS = [(.15, 0, .5), (.6, 0, .5)]
HEAD_HPR_SCALE = (160, -20, 0, .15, .15, .15)

# Grim Make a Toon limbs
BASE_LIMB_SCALE = .125
LIMB_POS = { # Left to right.
    'leg-s': [(-.75, 0, .5), (-.45, 0, .5), (-.15, 0, .5)],
    'leg-m': [(-.75, 0, -.05), (-.45, 0, -.05), (-.15, 0, -.05)],
    'leg-l': [(.15, 0, 0), (.45, 0, 0), (.75, 0, 0)],

    'torso-s': [(-.75, 0, .605), (-.75, 0, .09), (.15, 0, .195)],
    'torso-m': [(-.445, 0, .63), (-.45, 0, .13), (.45, 0, .24)],
    'torso-l': [(-.15, 0, .675), (-.15, 0, .17), (.75, 0, .27)]
}
LIMB_SCALE = {
    'leg-s': (.15, BASE_LIMB_SCALE, .055),
    'leg-m': (BASE_LIMB_SCALE, BASE_LIMB_SCALE, .115),
    'leg-l': (BASE_LIMB_SCALE, BASE_LIMB_SCALE, .15),

    'torso-s': (.15, BASE_LIMB_SCALE, .125),
    'torso-m': (.075, BASE_LIMB_SCALE, .2),
    'torso-l': (.088, BASE_LIMB_SCALE, .175)
}
LIMB_HEAD_POS = [
    (-.75, 0, .715), (-.445, 0, .77), (-.145, 0, .845),
    (-.75, 0, .205), (-.445, 0, .275), (-.145, 0, .3425),
    (.15, 0, .31), (.45, 0, .39), (.75, 0, .448),
]