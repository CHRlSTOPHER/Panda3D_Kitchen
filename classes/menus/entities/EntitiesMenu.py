import json

from direct.gui.DirectButton import DirectButton
from direct.gui.DirectGui import DGG
from panda3d.core import Fog, Texture, Filename, NodePath
from direct.interval.IntervalGlobal import Sequence, Func, LerpFunc

from classes.settings import Globals as G
from classes.menus.entities.EntitiesMenuGUI import EntitiesMenuGUI
from classes.menus.entities.EntitiesMenuActor import EntitiesMenuActor
from classes.menus.entities.EntitiesMenuProp import EntitiesMenuProp
from classes.menus.entities.EntitiesMenuTexture import EntitiesMenuTexture
from classes.menus.entities.EntitiesMenuParticle import EntitiesMenuParticle
from classes.settings.FileManagement import get_resource_and_filename
from classes.startup.DisplayRegions import PREVIEW_REGION

DISABLED_COLOR = (.8, .8, .8, .8)
ENABLED_COLOR = (1.15, 1.15, 1.15, 1.2)
MODES = {
    'Actor': EntitiesMenuActor,
    'Prop': EntitiesMenuProp,
    'Texture': EntitiesMenuTexture,
    'Particle': EntitiesMenuParticle,
}


class EntitiesMenu(EntitiesMenuGUI):

    def __init__(self):
        EntitiesMenuGUI.__init__(self)

        self.mode = 'Actor'
        self.modes = {}
        self.mode_buttons = []
        self.library = None
        self.resources = G.RESOURCES

        # temporary until other sections have been developed.
        base.preview_region.set_dimensions(*PREVIEW_REGION)

        self.generate()

    def generate(self):
        for name, mode in MODES.items():
            self.modes[name] = mode()

        self.setup_fog()
        self.add_commands_to_buttons()
        self.set_mode('Actor', self.entity_mode_buttons['Actor'])

    def setup_fog(self):
        self.fog = Fog("Photo Fog") # Play on Photo Fun
        self.fog.set_color(1, 1, 1)
        self.fog.set_exp_density(0)
        base.preview_render.set_fog(self.fog)

    def add_commands_to_buttons(self):
        # 6 big entity buttons
        for name in self.entity_mode_buttons:
            button = self.entity_mode_buttons[name]
            button['command'] = self.set_mode
            button['extraArgs'] = [name, button]
            self.mode_buttons.append(button)

        self.selection_add['command'] = self.choose_file
        self.camera_button['command'] = self.handle_image_data
        self.modes[self.mode].define_rng_button(self.random_anim_button)

    def set_mode(self, mode, disable_button):
        # clean up any leftover assets
        self.modes[mode].cleanup_entity()
        # update the buttons that are enabled and disabled.
        self.change_button_colors(disable_button)
        # load the new data from the specified library.
        self.mode = mode
        self.reload_menu_selection()

    def choose_file(self):
        item_name, item_directory = get_resource_and_filename(
                                        title=f"Select {self.mode}",
                                        initialdir=self.resources)
        if not item_name: return

        # default to last used in future searches
        self.resources = ""
        self.check_for_anims()
        base.node_mover.set_clickability(True)
        self.modes[self.mode].cleanup_entity()
        self.modes[self.mode].load_entity(item_directory)
        self.item_name = item_name
        self.item_location = item_directory
        self.toggle_screenshot_button(True)

    def check_for_anims(self):
        if self.mode == 'Actor':
            anim_names, anim_dirs = get_resource_and_filename(
                title='Select Animations', initialdir=self.resources,
                multiple=True)
            self.modes['Actor'].set_anims(anim_names, anim_dirs)

    def reload_menu_selection(self):
        path = f"{G.DATABASE_DIRECTORY}{self.mode}Library.json"
        self.library = json.loads(open(path).read())

        # cleanup selection buttons
        for button in self.selection_buttons:
            button.destroy()

        if self.mode == 'Music' or self.mode == 'Sound':
            pass # will implement this later.
        else:
            self.load_picture_list()
        self.hide_special_buttons() # buttons used for specific modes

    def change_button_colors(self, disable_button):
        for button in self.mode_buttons: # enable click
            button['state'] = DGG.NORMAL
            button.set_color_scale(*DISABLED_COLOR)

        disable_button['state'] = DGG.DISABLED # disable click
        disable_button.set_color_scale(*ENABLED_COLOR)

    def handle_image_data(self):
        self.flash_screen() # play a camera flash animation
        # save the item to the library database of the specifed mode
        self.modes[self.mode].save_item(self.item_name, self.item_location)
        # capture an image of the model and save it
        self.capture_and_save_image()
        self.reload_menu_selection()

    def flash_screen(self):
        def flash(density):
            self.fog.set_exp_density(density)

        def fade(alpha):
            self.modes[self.mode].entity.set_alpha_scale(alpha)

        Sequence(
            LerpFunc(flash, duration=.35, fromData=0, toData=1),
            LerpFunc(flash, duration=.35, fromData=1, toData=0),
            LerpFunc(fade, duration=.3, fromData=1, toData=0),
            Func(self.modes[self.mode].cleanup_entity),
            Func(base.node_mover.set_clickability, True)
        ).start()

    def capture_and_save_image(self):
        if self.mode == "Music" or self.mode == "Sound":
            return # Nothing to capture and save

        buffer = base.win.make_texture_buffer("buffer", 128, 128, Texture(),
                                              to_ram=True)
        buffer.set_sort(-100)
        camera = base.make_camera(buffer)
        camera.node().get_lens().set_fov(G.PREVIEW_FOV)
        camera.reparent_to(base.preview_render)
        path = f"{G.R_EDITOR}{self.mode}/{self.item_name}.png"
        file_name = Filename.fromOsSpecific(path)

        base.graphicsEngine.render_frame()
        buffer.saveScreenshot(file_name)

    def toggle_screenshot_button(self, toggle):
        if toggle:
            self.camera_button.show()
        else:
            self.camera_button.hide()

    def hide_special_buttons(self):
        self.camera_button.hide()
        self.random_anim_button.hide()