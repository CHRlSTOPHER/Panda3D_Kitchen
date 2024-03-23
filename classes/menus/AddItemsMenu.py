import json
import tkinter as tk
from tkinter import filedialog

from direct.gui.DirectGui import DirectFrame, DirectButton, DGG
from direct.interval.IntervalGlobal import Sequence, LerpFunc, Func
from panda3d.core import Fog, TransparencyAttrib

from classes.props.PlaneModel import PlaneModel
from classes.settings.FileManagement import (get_resource_dir_and_file_name,
                                             update_database_library)
from classes.settings import Globals as G

FRAME_POS = (-1.5, 0, -.5)
FRAME_SCALE = (-.295, .5, .5)

ADD_POS = (.03, 0, -.865)
ADD_SCALE = (.24, .24, .19)

ADD_BUTTON = "_add_button"

MODES = { # Keyword, pos, padding
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

        self.allow_screenshot = False
        self.file_location = None
        self.mode = 'Actor'
        self.keyword = None
        self.buttons = []

        self.preview_model = None
        self.item_name = None
        self.item_location = None
        self.fog = None

        # define all the mode classes
        self.modes = {
            'Actor': ActorMode(),
            'Prop': PropMode(),
            'Music': MusicMode(),
            'Sound': SoundMode(),
            'Texture': TextureMode(),
            'Particle': ParticleMode(),
        }

        # Start the search in the root of the resources file.
        json_settings = json.loads(open(G.SETTINGS_JSON).read())
        self.resources = json_settings['project-path'] + G.RESOURCES

        self.screenshot_sfx = loader.load_sfx(G.SFX_4 + "Photo_shutter.ogg")
        self.screenshot_sfx.set_balance(-.25)

        # Load the top and bottom buttons. The other buttons are dynamic.
        self.load_buttons()
        self.set_mode("Actor", "last-actor", self.buttons[0])
        self.setup_fog()

    def load_buttons(self):
        category_frame = DirectFrame(parent=self, pos=(-.015, 0, -.07),
                                     scale=(1.11, 1.11, 1.11))
        for category in MODES:
            mode = MODES[category][0]
            keyword = MODES[category][1]
            pos = MODES[category][2]
            padding = MODES[category][3]
            button = DirectButton(text=category, parent=category_frame,
                                  pad=padding, pos=pos, scale=(-.15, .15, .1),
                                  command=self.set_mode)
            button['extraArgs'] = [mode, keyword, button]
            self.buttons.append(button)

        # This button lets you choose a file to add to the preview region.
        self.add_button = DirectButton(text="+", parent=self, pad=(1.7, .05),
                                       pos=ADD_POS, scale=ADD_SCALE,
                                       command=self.choose_file)

        # This is the button that will take the screenshot and save to file.
        self.camera_button = DirectButton(text="[(*)]", parent=self,
                                          pos=(-.75, 0, -.85),
                                          scale=(.3, .15, .15),
                                          command=self.take_screenshot)
        self.toggle_screenshot_button()

    def set_mode(self, mode, keyword, selected_button):
        # cleanup existing item if one exists before changing modes.
        self.modes[self.mode].cleanup_item()

        self.mode = mode
        self.keyword = keyword

        # enable all buttons
        for button in self.buttons:
            button['state'] = DGG.NORMAL
            button.set_color_scale(1, 1, 1, 1)

        # disable selected button
        selected_button['state'] = DGG.DISABLED
        selected_button.set_color_scale(.75, .75, .5, 1)

    def setup_fog(self):
        self.fog = Fog("Photo Fog") # Play on Photo Fun
        self.fog.set_color(1, 1, 1)
        base.preview_render.set_fog(self.fog)

    def choose_file(self):
        # temporary hard coded value for testing.
        self.resources = "C:/Users/Chris/Desktop/Panda3D_Kitchen/resources/phase_4/models/char"

        item_name, item_directory = get_resource_dir_and_file_name(
                                            title=f"Select {self.mode}",
                                            initialdir=self.resources)

        # we need to ask a second time for actor animations
        if self.mode == 'Actor':
            anim_names, anim_directories = get_resource_dir_and_file_name(
                title='Select Animations', initialdir=self.resources,
                multiple=True)
            self.modes[self.mode].set_anims(anim_names, anim_directories)

        # for future searches, fallback on last directory used.
        self.resources = ""

        if item_directory == "":
            return # ignore user cancel input

        self.item_name = item_name

        # The load method will vary based on the mode.
        self.modes[self.mode].load_item(item_directory)
        self.item_location = item_directory # store this variable for later

    def take_screenshot(self):
        self.toggle_screenshot_button()

        # play short animation and remove preview model
        self.flash_screen()

        # The save method will vary based on the mode.
        self.modes[self.mode].save_item(self.item_name, self.item_location)

    def flash_screen(self):
        self.preview_model.set_transparency(TransparencyAttrib.MDual)
        def flash(density):
            self.fog.set_exp_density(density)

        def fade(alpha):
            self.preview_model.set_alpha_scale(alpha)

        Sequence(
            Func(self.screenshot_sfx.play),
            LerpFunc(flash, duration=.5, fromData=0, toData=1),
            LerpFunc(flash, duration=.5, fromData=1, toData=0),
            LerpFunc(fade, duration=.4, fromData=1, toData=0, blendType='easeOut'),
            Func(self.preview_model.remove_node)
        ).start()

    def save_item_to_file(self):
        icon_path = f'{G.R_EDITOR}/{self.mode}/{self.item_name}.jpg'
        base.screenshot(namePrefix=icon_path, defaultFilename=0,
                        source=base.preview_region)
        update_database_library(self.mode, self.item_location, self.item_name)

    def toggle_screenshot_button(self, force=None):
        if force:
            self.allow_screenshot = True

        if self.allow_screenshot:
            self.camera_button['state'] = DGG.NORMAL
            self.camera_button.set_color_scale(1, 1, 1, 1)
        else:
            self.camera_button['state'] = DGG.DISABLED
            self.camera_button.set_color_scale(.25, .25, .25, 1)

        self.allow_screenshot = not self.allow_screenshot


# if you are confused why I have a cleanup and delete function-
# cleanup_item() cleans up items in the preview region when switching modes
# delete_item() removes the item from the library database.
class ActorMode():

    def __init__(self):
        self.anim_list = None

    def set_anims(self, anim_names, anim_dirs):
        self.anim_list = {}
        for i in range(0, len(anim_names)):
            self.anim_list[anim_names[i]] = anim_dirs[i]
        print(self.anim_list)

    def load_item(self, resource_location):
        pass

    def save_item(self):
        pass

    def cleanup_item(self):
        pass

    def delete_item(self):
        pass

class PropMode():

    def load_item(self, resource_location):
        pass

    def save_item(self):
        pass

    def cleanup_item(self):
        pass

    def delete_item(self):
        pass


class MusicMode():

    def load_item(self, resource_location):
        pass

    def save_item(self):
        pass

    def cleanup_item(self):
        pass

    def delete_item(self):
        pass


class SoundMode():

    def load_item(self, resource_location):
        pass

    def save_item(self):
        pass

    def cleanup_item(self):
        pass

    def delete_item(self):
        pass


class TextureMode():

    def load_item(self, resource_location):
        pass

    def save_item(self):
        pass

    def cleanup_item(self):
        pass

    def delete_item(self):
        pass


class ParticleMode():

    def load_item(self, resource_location):
        pass

    def save_item(self):
        pass

    def cleanup_item(self):
        pass

    def delete_item(self):
        pass
