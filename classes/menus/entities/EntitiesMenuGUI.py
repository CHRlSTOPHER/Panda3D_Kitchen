from direct.gui.DirectGui import (DirectFrame, DirectButton,
                                  DirectScrolledFrame, DGG)
from panda3d.core import PGButton, MouseButton
from classes.props.PlaneModel import PlaneModel

ENTITY_MODE_BUTTONS = [
    ["Actor", (0.356, 0.0, -0.615), (0.145, 0.148, 0.151), (0.087, 0.0)],
    ["Prop", (0.734, 0.0, -0.615), (0.169, 0.175, 0.178), (-0.045, -0.162)],
    ["Music", (1.115, 0.0, -0.615), (0.154, 0.154, 0.151), (0.039, -0.003)],
    ["Sound", (1.49, 0.0, -0.615), (0.154, 0.154, 0.148), (0.033, 0.03)],
    ["Texture", (1.874, 0.0, -0.615), (0.169, 0.169, 0.166), (0, -0.096)],
    ["Particle", (2.252, 0.0, -0.615), (0.16, 0.181, 0.169), (-0.021, -0.108)],
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

        self.load_gui()
        self.bind_gui()

    def load_gui(self):
        # The 6 entity buttons
        for text, pos, scale, pad in ENTITY_MODE_BUTTONS:
            geom = PlaneModel(f'editor/maps/add-{text}.png')
            pos = (pos[0] - .76, pos[1], pos[2])  # adjust x
            button = DirectButton(parent=self, geom=geom,
                                  pos=pos, scale=scale, pad=pad)
            self.entity_mode_buttons[text] = button

        # Scene Objects Menu
        self.scene_text = DirectFrame(parent=self, text="SCENE OBJECTS",
                                      pos=(-1.215, 0.0, 0.843),
                                      scale=(0.103, 0.115, 0.109))
        self.scene_scroll = DirectScrolledFrame(self,
                                        pos=(-1.213, 0.0, 0.495),
                                        scale=(0.889, 0.955, 0.655),
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
                                          pos=(-1.215, 0.0, -0.078),
                                          scale=(0.103, 0.115, 0.103))
        self.selection_scroll = DirectScrolledFrame(parent=self,
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

        geom = PlaneModel(f'editor/maps/add-Camera.png')
        self.camera_button = DirectButton(parent=self, geom=geom,
                                          pos=(0.035, 0.0, -.226),
                                          scale=(0.16, 0.181, 0.169),
                                          pad=(-0.021, -0.108))
        self.camera_button.set_color_scale(1, 1, 1, .75)
        self.camera_button.hide()

    def bind_gui(self):
        self.scene_scroll['state'] = DGG.NORMAL
        self.selection_scroll['state'] = DGG.NORMAL
        self.scene_scroll.bind(DGG.WHEELUP, self.scroll_scene_up)
        self.scene_scroll.bind(DGG.WHEELDOWN, self.scroll_scene_down)
        self.selection_scroll.bind(DGG.WHEELUP, self.selection_scroll_up)
        self.selection_scroll.bind(DGG.WHEELDOWN, self.selection_scroll_down)

    def scroll_scene_up(self, mouse_data):
        self.scene_scroll[VALUE] -= 1

    def scroll_scene_down(self, mouse_data):
        self.scene_scroll[VALUE] += 1

    def selection_scroll_up(self, mouse_data):
        self.selection_scroll[VALUE] -= 1

    def selection_scroll_down(self, mouse_data):
        self.selection_scroll[VALUE] += 1