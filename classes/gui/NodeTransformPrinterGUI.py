from direct.gui.DirectGui import DirectButton
from panda3d.core import TextNode

from classes.globals import Globals as G
from classes.globals import GUIGlobals as GG


class NodeTransformPrinterGUI():

    def __init__(self, node_mover, func_printer): # TransformFunctionPrinter
        self.node_mover = node_mover
        self.func_printer = func_printer
        self.printer_buttons = []

        self.append_printer_buttons()

    def append_printer_buttons(self):
        z = GG.TF_BUTTON_Z
        for index in range(0, len(G.TRANSFORM_FUNCTION_STRINGS)):
            button = self.generate_printer_button(index)
            button.reparent_to(base.a2dTopCenterNs)
            button.set_pos(GG.TF_BUTTON_X, 0, z)
            button.set_scale(GG.TF_BUTTON_SCALE)
            self.printer_buttons.append(button)
            z += GG.TF_BUTTON_Z_INCREMENT

    def generate_printer_button(self, index):
        return DirectButton(
            text = G.TRANSFORM_FUNCTION_NAMES[index],
            text_align = TextNode.ALeft,
            command = self.print_tranform, extraArgs = [index]
        )

    def print_tranform(self, index):
        self.func_printer.update_transform_data(self.node_mover)
        self.func_printer.print_transform_func(index)