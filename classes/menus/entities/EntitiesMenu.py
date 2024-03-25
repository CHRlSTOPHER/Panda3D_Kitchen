from direct.gui.DirectGui import DGG

from classes.menus.entities.EntitiesMenuGUI import EntitiesMenuGUI
from classes.menus.entities.EntitiesMenuActor import EntitiesMenuActor
from classes.menus.entities.EntitiesMenuProp import EntitiesMenuProp
from classes.menus.entities.EntitiesMenuMusic import EntitiesMenuMusic
from classes.menus.entities.EntitiesMenuSound import EntitiesMenuSound
from classes.menus.entities.EntitiesMenuTexture import EntitiesMenuTexture
from classes.menus.entities.EntitiesMenuParticle import EntitiesMenuParticle

ENABLED_COLOR = (1, 1, 1, 1)
DISABLED_COLOR = (.5, .5, .5, 1)
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

        self.add_commands_to_buttons()
        self.set_mode('Actor', self.entity_mode_buttons['Actor'])

    def add_commands_to_buttons(self):
        for name in self.entity_mode_buttons:
            button = self.entity_mode_buttons[name]
            button['command'] = self.set_mode
            button['extraArgs'] = [name, button]
            self.mode_buttons.append(button)

    def set_mode(self, mode, disable_button):
        for button in self.mode_buttons: # enable click
            button['state'] = DGG.NORMAL
            button.set_color_scale(*DISABLED_COLOR)

        disable_button['state'] = DGG.DISABLED # disable click
        disable_button.set_color_scale(*ENABLED_COLOR)

        self.mode = mode