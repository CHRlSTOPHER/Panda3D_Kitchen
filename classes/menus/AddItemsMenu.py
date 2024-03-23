import json
import tkinter as tk
from tkinter import filedialog

from direct.gui.DirectGui import DirectFrame, DirectButton, DGG

from classes.props.PlaneModel import PlaneModel
from classes.settings.FileManagement import (FILES_JSON,
                                             get_directory_and_resource_dir)
from classes.windows.NewWindow import NewWindow
from classes.settings import Globals as G

FRAME_POS = (-1.5, 0, -.5)
FRAME_SCALE = (-.295, .5, .5)

ADD_POS = (.03, 0, -.865)
ADD_SCALE = (.24, .24, .19)

ADD_BUTTON = "_add_button"

CATEGORIES = { # Keyword, pos, padding
    "ACTORS": ['Actor', 'last-actor', (.478, 0, .8), (.49, 0)],
    "PROPS": ['Prop', 'last-prop', (-.31, 0, .8), (.99, 0)],
    "MUSIC": ['Music', 'last-music', (.481, 0, .69), (.92, 0)],
    "SOUNDS": ['Sound', 'last-sound', (-.313, 0, .69), (.53, 0)],
    "TEXTURES": ['Texture', 'last-texture', (.478, 0, .58), (0, 0)],
    "PARTICLES": ['Particle', 'last-particle', (-.31, 0, .58), (0, 0)],
}


class AddItemsMenu(DirectFrame):

    def __init__(self):
        frame = PlaneModel("resources/editor/maps/handle.png")
        DirectFrame.__init__(self, geom=frame,
                             pos=FRAME_POS, scale=FRAME_SCALE)
        self.initialiseoptions(AddItemsMenu)

        self.file_location = None
        self.mode = None
        self.keyword = None
        self.buttons = []
        self.allow_screenshot = False
        self.item_name = None

        # Start the search in the root of the resources file.
        json_settings = json.loads(open(G.SETTINGS_JSON).read())
        self.resources = json_settings['project-path'] + "resources/"

        self.load_buttons()
        self.set_mode("Actor", "last-actor", self.buttons[0])

    def load_buttons(self):
        category_frame = DirectFrame(parent=self, pos=(-.015, 0, -.07),
                                     scale=(1.11, 1.11, 1.11))
        for category in CATEGORIES:
            mode = CATEGORIES[category][0]
            keyword = CATEGORIES[category][1]
            pos = CATEGORIES[category][2]
            padding = CATEGORIES[category][3]
            button = DirectButton(text=category, parent=category_frame,
                                  pad=padding, pos=pos, scale=(-.15, .15, .1),
                                  command=self.set_mode)
            button['extraArgs'] = [mode, keyword, button]
            self.buttons.append(button)

        self.add_button = DirectButton(text="+", parent=self, pad=(1.7, .05),
                                       pos=ADD_POS, scale=ADD_SCALE,
                                       command=self.choose_file)
        self.camera_button = DirectButton(text="[(*)]", parent=self,
                                          state=DGG.DISABLED,
                                          pos=(-.75, 0, -.85),
                                          scale=(.3, .15, .15),
                                          command=self.take_screenshot)
        self.camera_button.set_color_scale(.25, .25, .25, 1)

    def set_mode(self, mode, keyword, selected_button):
        self.mode = mode
        self.keyword = keyword

        # enable all buttons
        for button in self.buttons:
            button['state'] = DGG.NORMAL
            button.set_color_scale(1, 1, 1, 1)

        # disable selected button
        selected_button['state'] = DGG.DISABLED
        selected_button.set_color_scale(.75, .75, .5, 1)

    def choose_file(self):
        self.resources = "C:/Users/Chris/Desktop/Panda3D_Kitchen/resources/phase_4/models/char"
        resource_location, item_name = get_directory_and_resource_dir(
                                            initialdir=self.resources)
        # for future searches, fallback on last directory used.
        self.resources = ""

        if resource_location == "":
            return # ignore user cancel input

        self.item_name = item_name

        self.load_model_for_screenshot(resource_location)
        self.save_item_to_file(resource_location)

    def load_model_for_screenshot(self, resource_location):
        self.preview_model = loader.load_model(resource_location)
        self.preview_model.set_y(5)
        self.preview_model.reparent_to(base.preview_render)
        base.node_mover.set_node(self.preview_model)

        self.camera_button['state'] = DGG.NORMAL
        self.camera_button.set_color_scale(1, 1, 1, 1)

    def take_screenshot(self):
        icon_path = f'{G.R_EDITOR}/{self.mode}/{self.item_name}.jpg'
        base.screenshot(namePrefix=icon_path, defaultFilename=0,
                        source=base.preview_region)
        self.camera_button['state'] = DGG.DISABLED
        self.camera_button.set_color_scale(.25, .25, .25, 1)
        self.preview_model.remove_node()

    def save_item_to_file(self, resource_location):
        pass