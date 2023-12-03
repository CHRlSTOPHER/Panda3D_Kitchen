"""
This is a collection of different classes and mashes them all together into an editor. WIP.
"""
from panda3d.core import WindowProperties

from classes.gui.NodeEditorGUI import NodeEditorGUI
from .NodeMover import NodeMover
from .NodeSelector import NodeSelector
from .TransformFunctionPrinter import TransformFunctionPrinter, get_transform_data
from classes.gui.DataPrinterWindow import DataPrinterWindow


class NodeEditor(NodeEditorGUI):

    def __init__(self):
        NodeEditorGUI.__init__(self)
        # Set the camera as the default node. It can be changed later through selection.
        self.node_mover = NodeMover(camera)
        self.node_selector = NodeSelector(self.node_mover)
        self.tf_printer = TransformFunctionPrinter(*get_transform_data(camera))

        self.dp_window = DataPrinterWindow(self.node_mover, self.tf_printer)

        # set the main window in the foreground
        wp = WindowProperties()
        wp.set_foreground(True)
        base.win.requestProperties(wp)

    def cleanup(self):
        self.node_mover.cleanup()
        self.node_selector.cleanup()