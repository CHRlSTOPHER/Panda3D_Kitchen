from classes.settings import Globals as G

FILE = "FILE"
BODY = "TOON"
BUCKET = "PAINTBUCKET"
WARDROBE = "WARDRODE"
NAME = "NAME"

BUCKET_MODEL = G.APP_MODELS + "paint-bucket" + G.EGG
WARDROBE_MODEL = G.ESTATE_5_5 + "closetBoy" + G.BAM

CAMERA_POS, CAMERA_HPR = [(-5.87, 9.83, 5.64), (-137.99, -12.87, 0.0)]
TOON_POS, TOON_HPR = [(-0.56, -1.02, 0.0), (0, 0, 0)]
BUCKET_POS, BUCKET_HPR = [(0.19, -6.66, 0.0), (90.7, -3.0, 5.25)]
WARDROBE_POS, WARDROBE_HPR = [(3.85, -4.83, -0.15), (-132.32, 0.0, 0.0)]

GUI_INTERVALS = {
    BODY: [(-1, 0, 0)],
    BUCKET: [(-1, 0, 0)],
    WARDROBE: [(-1, 0, 0)],
}

FRAME_TEXTURE = G.APP_MAPS + "mat_panel"
LASHES_TEXTURE = G.APP_MAPS + "lashes-buttons" + G.PNG
BOTTOMS_TEXTURE = G.APP_MAPS + "bottoms-buttons" + G.PNG
SPECIES_TEXTURE = G.APP_MAPS + "toon-species-buttons" + G.JPG
LIMB_TEXTURE = G.APP_MAPS + "limb-sizes" + G.PNG
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
UNSORTED_EYES = {'d': ["eyes"], 'r': ["eyes"], 'p': ["eyes-short", "eyes-long"]}
UNSORTED_PUPILS = {
    'd': ["def_left_pupil", "def_right_pupil"],
    'r': ["joint_pupilL_long", "joint_pupilR_long",
          "joint_pupilL_short", "joint_pupilR_short"],
    'p': ["joint_pupilL_long", "joint_pupilR_long",
          "joint_pupilL_short", "joint_pupilR_short"]
}

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