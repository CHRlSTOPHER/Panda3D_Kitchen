"""
A collection of different classes. Mashes them together into an editor.
"""
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectFrame

from classes.camera.RotationalCamera import RotationalCamera
from classes.camera.FovScrollWheel import FovScrollWheel
from .NodeMover import NodeMover
from .NodeSelector import NodeSelector
from .NodeTransformPrinter import (NodeTransformPrinter, get_transform_data)
from classes.gui.NodeTransformPrinterGUI import NodeTransformPrinterGUI
from .SequenceManager import SequenceManager


class MasterEditor(DirectObject):

    def __init__(self, rot_cam=True, nt_printer=True, fov=50, sequence=None):
        DirectObject.__init__(self)
        self.hide_gui = False
        self.accept("`", self.hide_editor_gui)

        self.rot_cam = None
        self.nt_printer = None
        self.nt_gui = None

        self.fov_wheel = FovScrollWheel(fov)
        self.node_mover = NodeMover(camera)
        self.node_selector = NodeSelector(self.node_mover)

        if rot_cam:
            self.rot_cam = RotationalCamera()

        if nt_printer:
            self.nt_printer = NodeTransformPrinter(*get_transform_data(camera))
            self.nt_gui = NodeTransformPrinterGUI(
                self.node_mover, self.nt_printer, base.a2dLeftCenter)

        if sequence:
           self.sequence_manager = SequenceManager(sequence)

    def hide_editor_gui(self):
        self.hide_gui = not self.hide_gui
        if self.hide_gui:
            aspect2d.hide() # hacky fix for now
        else:
            aspect2d.show()

    def get_node_mover(self):
        return self.node_mover

    def cleanup(self):
        classes = [self.node_mover, self.node_selector, self.fov_wheel]
        if self.orb_cam:
            classes.append(self.orb_cam)
        if self.nt_printer:
            classes.append(self.nt_printer)

        for class_item in classes:
            class_item.cleanup()