WINDOW_TITLE = "PANDA3D KITCHEN"

#json variable names
PROJECT_PATH = "project-path"
FULL_SCREEN = "full_screen"
WINDOW_SIZE = "window_size"
MONITOR_RES = "monitor_resolution"
BORDERLESS = "borderless"
BITS = "bits"
FRAMEBUFFER_MULTISAMPLE = "framebuffer-multisample"
MULTISAMPLES = "multisamples"
FPS_METER = "show_fps_meter"
AUTO_WALKER = "auto_walker"

FONTS = "phase_3/fonts/"

CHAR_3 = "phase_3/models/char/"
CHAR_3_5 = "phase_3.5/models/char/"
CHAR_4 = "phase_4/models/char"

MAPS_3 = "phase_3/maps/"
MAPS_3_5 = "phase_3.5/maps/"
MAPS_4 = "phase_4/maps/"

JPG = ".jpg"
EGG = ".egg"
BAM = ".bam"

ICON_FILENAME = "panda3d-chef.ico"
SETTINGS_JSON = 'settings.json'
KEYBINDINGS_JSON = "keybindings.json"

ORBITAL_CAM_MOUSE_SENSITIVITY = 70
FOV_MODIFIER = 90
FOV_SCROLL_AMOUNT = 5

ESCAPE = 'escape'
MOUSE_WHEEL_UP = 'wheel_up'
MOUSE_WHEEL_DOWN = "wheel_down"
LEFT_MOUSE_BUTTON = "mouse1"
MIDDLE_MOUSE_BUTTON = "mouse2"
RIGHT_MOUSE_BUTTON = "mouse3"

SPECIAL_NODE_IFIER_FLAG = "~"

BASE_FOV = 50.0
MINIMUM_SCROLL_FOV = 0
MAXIMUM_SCROLL_FOV = 180
TINY_DELAY = .001

AUTOWALKER_MOVE_ANIMS = ["walk", "run"]

RED = (1, 0, 0, 1)

TRANSFORM_FUNCTION_STRINGS = [
    None, # SET:
    "{name}.set_pos({x}, {y}, {z})",
    "{name}.set_hpr({h}, {p}, {r})",
    "{name}.set_scale({sx}, {sy}, {sz})",
    "{name}.set_pos_hpr_scale({x}, {y}, {z}, {h}, {p}, {r}, {sx}, {sy}, {sz})",
    "{name}.set_pos_hpr({x}, {y}, {z}, {h}, {p}, {r})",
    "base.camLens.set_fov({fov})",
    "",
    None, # FUNC:
    "Func({name}.set_pos_hpr, {x}, {y}, {z}, {h}, {p}, {r}),",
    "Func({name}.set_scale, {sx}, {sy}, {sz}),",
    "Func(base.camLens.set_fov, {fov}),",
    "",
    None, # LERPFUNC:
    "LerpFunc(base.camLens.set_fov, fromData=FOV_1, toData={fov},"
        "duration=DURATION, blendType='noBlend'),",
    "",
    None, # INTERVAL:
    "{name}.pos_hpr_interval(DURATION, ({x}, {y}, {z}), ({h}, {p}, {r}),"
        "blendType='easeInOut'),",
    "{name}.scale_interval(DURATION, ({sx}, {sy}, {sz}),"
        "blendType='easeInOut'),",
]
TRANSFORM_FUNCTION_NAMES = [
    "SET:",
    "POSITION",
    "ROTATION",
    "SCALE",
    "ALL THREE",
    "POS & HPR",
    "FOV",
    "",
    "FUNC:",
    "POS & HPR",
    "SCALE",
    "FOV",
    "",
    "LERPFUNC:",
    "FOV",
    "",
    "INTERVAL:",
    "POS & HPR",
    "SCALE",
]
# Node Mover
NM_SPEEDS = [
    ("speed_up", 0.33),
    ("slow_down", 2.25),
    ("snail_speed", 4.50),
]
NM_BASE_MOVE_RATE = .1
NM_BASE_TURN_RATE = .5

'''REGEX...
I KNOW i'm going to forgot what the hell these mean so i'll include an example

Find data between curly braces: "{([^}]+)}"
{: a literal curly brace
(: start capturing
[: start defining a class.
^}: anything other than }
]: end class definition
*: any number of characters that match the class we defined
): finish capturing
}: literal curly brace following what we captured

CREDIT - Kev on stackoverflow
URL:
https://stackoverflow.com/questions/
413071/regex-to-get-string-between-curly-braces/413085#413085
'''
FIND_ARGS_IN_CURLY_BRACES = "{([^}]+)}"