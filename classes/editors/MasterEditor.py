"""
This is a collection of different classes and mashes them all together into an editor. WIP.
"""
from panda3d.core import WindowProperties

from .NodeMover import NodeMover
from .NodeSelector import NodeSelector
from .TransformFunctionPrinter import (TransformFunctionPrinter,
                                       get_transform_data)
from classes.windows.TransformFuncWindow import TransformFuncWindow
from classes.windows.PropGeneratorWindow import PropGeneratorWindow


class MasterEditor():

    def __init__(self):
        # Set camera as default node. It can be changed later by selection.
        self.node_mover = NodeMover(camera)
        self.node_selector = NodeSelector(self.node_mover)
        self.tf_printer = TransformFunctionPrinter(*get_transform_data(camera))

        self.dp_window = TransformFuncWindow(self.node_mover, self.tf_printer)
        self.pg_window = PropGeneratorWindow(self.node_mover)

        # set the main window in the foreground
        wp = WindowProperties()
        wp.set_foreground(True)
        base.win.requestProperties(wp)

    def cleanup(self):
        self.node_mover.cleanup()
        self.node_selector.cleanup()