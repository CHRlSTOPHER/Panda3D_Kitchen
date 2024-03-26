import json

from direct.gui.DirectGui import DGG

from classes.settings import Globals as G
from classes.menus.entities.EntitiesMenuGUI import EntitiesMenuGUI
from classes.menus.entities.EntitiesMenuActor import EntitiesMenuActor
from classes.menus.entities.EntitiesMenuProp import EntitiesMenuProp
from classes.menus.entities.EntitiesMenuMusic import EntitiesMenuMusic
from classes.menus.entities.EntitiesMenuSound import EntitiesMenuSound
from classes.menus.entities.EntitiesMenuTexture import EntitiesMenuTexture
from classes.menus.entities.EntitiesMenuParticle import EntitiesMenuParticle
from classes.settings.FileManagement import get_resource_and_filename

DISABLED_COLOR = (.8, .8, .8, .8)
ENABLED_COLOR = (1.15, 1.15, 1.15, 1.2)
MODES = {
    'Actor': EntitiesMenuActor(),
    'Prop': EntitiesMenuProp(),
    'Music': EntitiesMenuMusic(),
    'Sound': EntitiesMenuSound(),
    'Texture': EntitiesMenuTexture(),
    'Particle': EntitiesMenuParticle(),
}


class EntitiesMenu(EntitiesMenuGUI):

    def __init__(self):
        EntitiesMenuGUI.__init__(self)

        self.mode = 'Actor'
        self.modes = MODES
        self.mode_buttons = []
        self.library = None
        self.resources = G.RESOURCES

        self.add_commands_to_buttons()
        self.set_mode('Actor', self.entity_mode_buttons['Actor'])

    def add_commands_to_buttons(self):
        # 6 big entity buttons
        for name in self.entity_mode_buttons:
            button = self.entity_mode_buttons[name]
            button['command'] = self.set_mode
            button['extraArgs'] = [name, button]
            self.mode_buttons.append(button)

        # bottom add and remove button
        self.selection_add['command'] = self.choose_file
        # self.selection_remove['command'] = self.remove_file()

    def set_mode(self, mode, disable_button):
        # clean up any leftover assets
        MODES[mode].cleanup_entity()
        # update the buttons that are enabled and disabled.
        self.change_button_colors(disable_button)
        # load the new data from the specified library.
        self.reload_menu_selection(mode)
        self.mode = mode

    def choose_file(self):
        item_name, item_directory = get_resource_and_filename(
                                        title=f"Select {self.mode}",
                                        initialdir=self.resources)
        if not item_name: return

        # default to last used in future searches
        self.resources = ""
        self.check_for_anims()
        base.node_mover.set_clickability(True)
        MODES[self.mode].cleanup_entity()
        MODES[self.mode].load_entity(item_directory)
        self.item_name = item_name
        self.item_location = item_directory
        self.toggle_screenshot_button(True)

    def check_for_anims(self):
        if self.mode == 'Actor':
            anim_names, anim_dirs = get_resource_and_filename(
                title='Select Animations', initialdir=self.resources,
                multiple=True)
            MODES['Actor'].set_anims(anim_names, anim_dirs)

    def reload_menu_selection(self, mode):
        path = f"{G.DATABASE_DIRECTORY}{mode}Library.json"
        self.library = json.loads(open(path).read())

    def change_button_colors(self, disable_button):
        for button in self.mode_buttons: # enable click
            button['state'] = DGG.NORMAL
            button.set_color_scale(*DISABLED_COLOR)

        disable_button['state'] = DGG.DISABLED # disable click
        disable_button.set_color_scale(*ENABLED_COLOR)

    def toggle_screenshot_button(self, toggle):
        if toggle:
            self.camera_button.show()
        else:
            self.camera_button.hide()