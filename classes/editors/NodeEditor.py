"""
This is a collection of different classes and mashes them all together into an editor. WIP.
"""
from classes.gui.DataPrinterWindow import DataPrinterWindow
from classes.gui.NodeEditorGUI import NodeEditorGUI
from .NodeMover import NodeMover
from .NodeSelector import NodeSelector
from .TransformFunctionPrinter import TransformFunctionPrinter, get_transform_data


class NodeEditor(NodeEditorGUI, DataPrinterWindow):

    def __init__(self):
        NodeEditorGUI.__init__(self)
        DataPrinterWindow.__init__(self)
        # Set the camera as the default node. It can be changed later through selection.
        self.node_mover = NodeMover(camera)
        self.node_selector = NodeSelector(self.node_mover)
        self.tf_printer = TransformFunctionPrinter(*get_transform_data(camera))

        self.accept("9", self.print_data_for_current_node)

    def print_data_for_current_node(self):
        self.tf_printer.update_transform_data(self.node_mover)
        function_print_index = 4 # test. I'll implement ui for printing data later
        self.tf_printer.print_transform_func(function_print_index)

    def cleanup(self):
        self.node_mover.cleanup()
        self.node_selector.cleanup()