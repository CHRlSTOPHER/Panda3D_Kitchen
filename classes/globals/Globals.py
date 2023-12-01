# Change project path to the filepath you saved the project to.
WINDOW_TITLE = "PANDA3D KITCHEN"
ICON_FILENAME = "panda3d-chef.ico"
SETTINGS_JSON = 'settings.json'
KEYBINDINGS_JSON = "keybindings.json"

ORBITAL_CAM_MOUSE_SENSITIVITY = 70
FOV_MODIFIER = 90
FOV_SCROLL_AMOUNT = 6

ESCAPE = 'escape'
MOUSE_WHEEL_UP = 'wheel_up'
MOUSE_WHEEL_DOWN = "wheel_down"
LEFT_MOUSE_BUTTON = "mouse1"
MIDDLE_MOUSE_BUTTON = "mouse2"
RIGHT_MOUSE_BUTTON = "mouse3"

ORB_CAM_TASK = "orb_cam_task"
RAY_MOUSE_TASK = 'ray_mouse_task'

BASE_FOV = 50.0
MINIMUM_SCROLL_FOV = 0
MAXIMUM_SCROLL_FOV = 180
TINY_DELAY = .001

RED = (1, 0, 0, 1)

TRANSFORM_FUNCTION_STRINGS = [
    "{name}.set_pos({x}, {y}, {z})",
    "{name}.set_hpr({h}, {p}, {r})",
    "{name}.set_scale({sx}, {sy}, {sz})",
    "{name}.set_pos_hpr({x}, {y}, {z}, {h}, {p}, {r})",
    "{name}.set_pos_hpr_scale({x}, {y}, {z}, {h}, {p}, {r}, {sx}, {sy}, {sz})",

    "Func({name}.set_pos_hpr, {x}, {y}, {z}, {h}, {p}, {r}),",
    "Func({name}.set_scale, {sx}, {sy}, {sz}),",

    "{name}.pos_hpr_interval(DURATION, ({x}, {y}, {z}), ({h}, {p}, {r}), blendType='easeInOut'),",
    "{name}.scale_interval(DURATION, ({sx}, {sy}, {sz}), blendType='easeInOut'),",

    "{name}: [{x}, {y}, {z}, {h}, {p}, {r}]",
    "{name}: [{sx}, {sy}, {sz}]",

    "base.camLens.set_fov({fov})",
    "Func(base.camLens.set_fov, {fov}),",
    "LerpFunc(base.camLens.set_fov, fromData=FOV_1, toData={fov}, duration=DURATION, blendType='noBlend'),",
]

# NM is short for Node Mover
NM_TRANSFORM_INPUTS = [
    "move_forward", # +y
    "move_back",    # -y
    "move_left",    # -x
    "move_right",   # +x
    "move_up",      # +z
    "move_down",    # -z

    "turn_back",             # +p
    "turn_forward",          # -p
    "turn_left_horizontal",  # +h
    "turn_right_horizontal", # -h
    "turn_right_vertical",   # +r
    "turn_left_vertical",    # -r
]
NM_SPEEDS = [
    ("speed up", 0.33),
    ("slow down", 2.5),
    ("snail speed", 5.0),
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
URL: https://stackoverflow.com/questions/413071/regex-to-get-string-between-curly-braces/413085#413085
'''
FIND_ARGS_IN_CURLY_BRACES = "{([^}]+)}"