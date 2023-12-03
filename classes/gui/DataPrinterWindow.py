from direct.gui.DirectGui import DirectButton
from direct.showbase.DirectObject import DirectObject
from panda3d.core import TextNode

from classes.render.NewWindow import NewWindow
from classes.globals import Globals as G
from classes.globals import GUIGlobals as GG

BUTTON_X = -.4
DPW_Z_INCREMENT = -.1


class DataPrinterWindow(NewWindow):

    def __init__(self, node_mover, func_printer): # TransformFunctionPrinter
        self.generate_window()

        self.node_mover = node_mover
        self.func_printer = func_printer
        self.printer_buttons = []

        self.append_printer_buttons()

    def generate_window(self):
        properties = base.win.getProperties()
        decorated = str(properties).split()[6]
        if decorated == "undecorated":
            NewWindow.__init__(self, GG.DP_WINDOW_ORIGIN_B_LESS, GG.DP_WINDOW_SIZE_B_LESS)
        else:
            NewWindow.__init__(self, GG.DP_WINDOW_ORIGIN, GG.DP_WINDOW_SIZE)

    def append_printer_buttons(self):
        z = -.07
        for index in range(0, len(G.TRANSFORM_FUNCTION_NAMES)):
            button = self.generate_printer_button(index)
            button.reparent_to(self.a2dTopCenterNs)
            button.set_pos(BUTTON_X, 0, z)
            button.set_scale(GG.DP_BUTTON_SCALE)
            self.printer_buttons.append(button)
            z += DPW_Z_INCREMENT

    def generate_printer_button(self, index):
        return DirectButton(
            text = G.TRANSFORM_FUNCTION_NAMES[index], text_align = TextNode.ALeft,
            command = self.print_tranform, extraArgs = [index]
        )

    def print_tranform(self, index):
        self.func_printer.update_transform_data(self.node_mover)
        self.func_printer.print_transform_func(index)