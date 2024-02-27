"""
A collection of buttons that let you print out various bits of information
using the func_printer variable class being passed in.
"""
from direct.gui.DirectGui import DirectButton
from direct.gui import DirectGuiGlobals as DGG
from panda3d.core import TextNode, TransparencyAttrib

from classes.gui.Revealer import RevealerGUI
from classes.globals import Globals as G
from classes.globals import GUIGlobals as GG

ICON_TEXTURE = "windows/printer-icon.png"
ICON_SCALE = .15
ICON_ROTATE = 0
ICON_POS = (.15, 0, 0)
HIDE_POS = (-.6, 0, 0)

DETECTION_SCALE=(.5, 1, .8)
DETECTION_TEXTURE = "windows/handle.png"

BUTTON_START_Z = .625
BUTTON_X = .2
BUTTON_Z_INCREMENT = -.08
BUTTON_SCALE = (.075, 1, .06)
BUTTON_SHADOW = (.25, .2, 0, .75)

TITLE_TEXT_SCALE = (1.2, 1.2, 1.2)
UNDER_TEXT_SCALE = (1, 1, 1)
TITLE_COLOR = (1, .8, .2, 1)
UNDER_COLOR = (1, 1, .8, 1)
HIGHLIGHT = (1, .5, 0, 1)


class NodeTransformPrinterGUI(RevealerGUI):

    def __init__(self, node_mover, func_printer, parent):
        RevealerGUI.__init__(self, ICON_TEXTURE, ICON_SCALE, ICON_POS,
                             DETECTION_TEXTURE, 180, DETECTION_SCALE,
                             HIDE_POS, parent)
        self.node_mover = node_mover
        self.func_printer = func_printer
        self.printer_buttons = []
        self.text_font = loader.load_font(G.FONTS + GG.CAFE_FONT)

        self.append_printer_buttons()

    def append_printer_buttons(self):
        z = BUTTON_START_Z
        for index in range(0, len(G.TRANSFORM_FUNCTION_STRINGS)):
            if G.TRANSFORM_FUNCTION_STRINGS[index] == "":
                z += BUTTON_Z_INCREMENT / 2.0
                continue
            button = self.generate_printer_button(index)
            button.bind(DGG.WITHIN, self.highlight_text, extraArgs=[button])
            button.bind(DGG.WITHOUT, self.darken_text, extraArgs=[button])
            button.set_pos(BUTTON_X, 0, z)
            self.printer_buttons.append(button)
            z += BUTTON_Z_INCREMENT

    def generate_printer_button(self, index,
                                text_scale=TITLE_TEXT_SCALE,
                                text_fg=TITLE_COLOR,
                                command=None, state=DGG.DISABLED):
        name = G.TRANSFORM_FUNCTION_STRINGS[index]
        if name and name != "":
            command = self.print_tranform
            state = DGG.NORMAL
            text_scale = UNDER_TEXT_SCALE
            text_fg = UNDER_COLOR

        button =  DirectButton(
            parent=self, scale=BUTTON_SCALE,
            text = G.TRANSFORM_FUNCTION_NAMES[index], text_fg=text_fg,
            text_align = TextNode.ACenter, text_font = self.text_font,
            text_scale=text_scale, text_shadow=BUTTON_SHADOW,
            frameVisibleScale=(0, 0), state=state,
            command = command, extraArgs = [index]
        )
        button.set_transparency(TransparencyAttrib.MBinary)
        return button

    def highlight_text(self, button, entry):
        button['text_fg'] = HIGHLIGHT

    def darken_text(self, button, entry):
        button['text_fg'] = UNDER_COLOR

    def print_tranform(self, index):
        self.func_printer.update_transform_data(self.node_mover)
        self.func_printer.print_transform_func(index)