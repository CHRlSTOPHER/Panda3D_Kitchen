"""
This is a collection of different classes and mashes them all together into an editor. WIP.
"""
from panda3d.core import WindowProperties

from .NodeMover import NodeMover
from .NodeSelector import NodeSelector
from .NodeTransformPrinter import (NodeTransformPrinter, get_transform_data)
from classes.gui.NodeTransformPrinterGUI import NodeTransformPrinterGUI
from classes.windows.LockMouseInWindow import LockMouseInWindow


class MasterEditor():

    def __init__(self):
        self.mouse_lock = LockMouseInWindow()

        # Set camera as default node. It can be changed later by selection.
        self.node_mover = NodeMover(camera)
        self.node_selector = NodeSelector(self.node_mover)
        self.nt_printer = NodeTransformPrinter(*get_transform_data(camera))

        self.nt_gui = NodeTransformPrinterGUI(self.node_mover, self.nt_printer)

    def cleanup(self):
        self.node_mover.cleanup()
        self.node_selector.cleanup()