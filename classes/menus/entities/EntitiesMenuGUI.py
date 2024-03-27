from direct.gui.DirectGui import (DirectFrame, DirectButton,
                                  DirectScrolledFrame, DGG)
from panda3d.core import PGButton, MouseButton

from classes.props.PlaneModel import PlaneModel
from classes.settings import Globals as G

BASE_CANVAS_SIZE = (-1, 1, -.87, 1)
CANVAS_LIMIT = 17
CANVAS_INCREMENT = .31
CAMERA_TEXTURE = f'editor/maps/capture-cam.png'
DICE_TEXTURE = f'editor/maps/rng-dice.png'

ENTITY_MODE_BUTTONS = [
    ["Actor", (0.734, 0.0, -0.615), (0.145, 0.148, 0.151), (0.087, 0.0)],
    ["Prop", (1.115, 0.0, -0.615), (0.169, 0.175, 0.178), (-0.045, -0.162)],
    ["Texture", (1.49, 0.0, -0.615), (0.169, 0.169, 0.166), (0, -0.096)],
    ["Particle", (1.874, 0.0, -0.615), (0.16, 0.181, 0.169), (-0.021, -0.108)],
]
DGG.WHEELUP = (PGButton.getPressPrefix() + MouseButton.wheel_up().getName()
               + '-')
DGG.WHEELDOWN = (PGButton.getPressPrefix() + MouseButton.wheel_down().getName()
              + '-')
VALUE = 'verticalScroll_value'


class EntitiesMenuGUI(DirectFrame):

    def __init__(self):
        DirectFrame.__init__(self)
        self.initialiseoptions(EntitiesMenuGUI)

        self.entity_mode_buttons = {}
        self.selection_buttons = []

        self.load_gui()
        self.bind_gui()

    def load_gui(self):
        self.entity_frame = DirectFrame(pos=(.44, 0, -.06), scale=.9)
        # The 6 entity buttons
        for text, pos, scale, pad in ENTITY_MODE_BUTTONS:
            geom = PlaneModel(f'editor/maps/add-{text}.png')
            pos = (pos[0] - .76, pos[1], pos[2])  # adjust x
            button = DirectButton(parent=self.entity_frame, geom=geom,
                                  pos=pos, scale=scale, pad=pad)
            self.entity_mode_buttons[text] = button

        # Scene Objects Menu
        self.scene_text = DirectFrame(parent=self, text="SCENE OBJECTS",
                                      pos=(-1.215, 0.0, 0.843),
                                      scale=(0.103, 0.115, 0.109))
        self.scene_scroll = DirectScrolledFrame(self,
                                        pos=(-1.213, 0.0, 0.495),
                                        scale=(0.889, 0.955, 0.655),
                                        canvasSize=BASE_CANVAS_SIZE,
                                        horizontalScroll_relief=None,
                                        horizontalScroll_incButton_relief=None,
                                        horizontalScroll_decButton_relief=None,
                                        horizontalScroll_thumb_relief=None)
        self.scene_remove = DirectButton(parent=self, text="-",
                                         pos=(-1.221, 0.0, 0.14),
                                         scale=(0.16, 0.16, 0.16),
                                         pad=(2.52, 0.084))

        # Menu Selection Menu
        self.menu_selection = DirectFrame(parent=self, text="MENU SELECTION",
                                          pos=(-1.213, 0.0, 0.495),
                                          scale=(0.103, 0.115, 0.103))
        self.selection_scroll = DirectScrolledFrame(parent=self,
                                        canvasSize=BASE_CANVAS_SIZE,
                                        horizontalScroll_relief=None,
                                        horizontalScroll_incButton_relief=None,
                                        horizontalScroll_decButton_relief=None,
                                        horizontalScroll_thumb_relief=None,
                                        pos=(-1.221, 0.0, -0.423),
                                        scale=(0.89, 0.955, 0.65))
        self.selection_add = DirectButton(parent=self, text="+",
                                          pos=(-1.459, 0.0, -0.765),
                                          scale=(0.151, 0.151, 0.151),
                                          pad=(1.113, -0.006))
        self.selection_remove = DirectButton(parent=self, text="-",
                                             pos=(-1.013, 0.0, -0.776),
                                             scale=(0.16, 0.16, 0.16),
                                             pad=(1.176, 0.084))

        geom = PlaneModel(CAMERA_TEXTURE)
        self.camera_button = DirectButton(parent=self, geom=geom,
                                          pos=(0.035, 0.0, -.226),
                                          scale=(0.16, 0.181, 0.169),
                                          pad=(-0.021, -0.108))
        self.camera_button.set_alpha_scale(.75)
        self.camera_button.hide()

        geom = PlaneModel(DICE_TEXTURE)
        self.random_anim_button = DirectButton(parent=self, geom=geom,
                                          pos=(1.025, 0.0, -.226),
                                          scale=(0.16, 0.181, 0.169),
                                          pad=(-0.021, -0.108))
        self.random_anim_button.set_alpha_scale(.75)
        self.random_anim_button.hide()

    def bind_gui(self):
        self.scene_scroll['state'] = DGG.NORMAL
        self.selection_scroll['state'] = DGG.NORMAL
        self.scene_scroll.bind(DGG.WHEELUP, self.scroll_scene_up)
        self.scene_scroll.bind(DGG.WHEELDOWN, self.scroll_scene_down)
        self.selection_scroll.bind(DGG.WHEELUP, self.selection_scroll_up)
        self.selection_scroll.bind(DGG.WHEELDOWN, self.selection_scroll_down)

    def load_picture_list(self):
        # reset canvas size when reloading
        self.selection_scroll['canvasSize'] = BASE_CANVAS_SIZE

        x, z, =[-.84, .84]
        i = 0
        for name in self.library:
            path = f"{G.R_EDITOR}{self.mode}/{name}.png"
            geom = PlaneModel(path)
            button = DirectButton(parent=self.selection_scroll.getCanvas(),
                                  geom=geom, pos=(x, 0, z), scale=.14)
            button.bind(DGG.WHEELUP, self.selection_scroll_up)
            button.bind(DGG.WHEELDOWN, self.selection_scroll_down)

            # modify the position of the button
            if x > -.3:
                x = -.84
                z -= CANVAS_INCREMENT
            else:
                x += .3

            # adjust the canvas size if the list is long 0_0
            if i > CANVAS_LIMIT:
                if i % 3 == 0:
                    bottom_size = self.selection_scroll['canvasSize'][2]
                    new_size = (-1, 1, bottom_size - CANVAS_INCREMENT, 1)
                    self.selection_scroll['canvasSize'] = new_size

            i += 1
            self.selection_buttons.append(button)
        # This makes scrolling down pretty much align with the icons.
        if i > 3:
            self.selection_scroll['verticalScroll_range'] = (0, int(i/4))

    def scroll_scene_up(self, mouse_data):
        self.scene_scroll[VALUE] -= 1

    def scroll_scene_down(self, mouse_data):
        self.scene_scroll[VALUE] += 1

    def selection_scroll_up(self, mouse_data):
        self.selection_scroll[VALUE] -= 1

    def selection_scroll_down(self, mouse_data):
        self.selection_scroll[VALUE] += 1