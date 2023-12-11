"""
A collection of different classes. Mashes them together into an editor.
"""
from direct.showbase.DirectObject import DirectObject

from classes.camera.OrbitalCamera import OrbitalCamera
from classes.camera.FovScrollWheel import FovScrollWheel
from .NodeMover import NodeMover
from .NodeSelector import NodeSelector
from .NodeTransformPrinter import (NodeTransformPrinter, get_transform_data)
from classes.gui.NodeTransformPrinterGUI import NodeTransformPrinterGUI
from classes.windows.LockMouseInWindow import LockMouseInWindow


class MasterEditor(DirectObject):

    def __init__(self):
        DirectObject.__init__(self)
        self.hide_gui = False
        self.accept("`", self.hide_editor_gui)

        # self.mouse_lock = LockMouseInWindow()
        # Set camera as default node. It can be changed later by selection.
        self.node_mover = NodeMover(camera)
        self.node_selector = NodeSelector(self.node_mover)
        self.nt_printer = NodeTransformPrinter(*get_transform_data(camera))
        self.orb_cam = OrbitalCamera()
        self.fov_wheel = FovScrollWheel()

        self.nt_gui = NodeTransformPrinterGUI(
            self.node_mover, self.nt_printer, base.a2dLeftCenter)

        self.gui_classes = [
            self.nt_gui,
        ]

    def hide_editor_gui(self):
        self.hide_gui = not self.hide_gui

        for _class in self.gui_classes:
            for gui in _class.guis:
                if self.hide_gui:
                    gui.hide()
                else:
                    gui.show()

    def cleanup(self):
        classes = [self.mouse_lock, self.node_mover, self.node_selector,
                   self.orb_cam, self.fov_wheel, self.nt_gui]
        for class_item in classes:
            class_item.cleanup()