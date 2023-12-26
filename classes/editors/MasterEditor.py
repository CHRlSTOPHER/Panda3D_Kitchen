"""
A collection of different classes. Mashes them together into an editor.
"""
from direct.showbase.DirectObject import DirectObject

from classes.camera.RotationalCamera import RotationalCamera
from classes.camera.FovScrollWheel import FovScrollWheel
from .NodeMover import NodeMover
from .NodeSelector import NodeSelector
from .NodeTransformPrinter import (NodeTransformPrinter, get_transform_data)
from classes.gui.NodeTransformPrinterGUI import NodeTransformPrinterGUI
from classes.gui.MouseWindowLock import MouseWindowLock


class MasterEditor(DirectObject):

    def __init__(self, mouse_lock=True, rot_cam=True, nt_printer=True):
        DirectObject.__init__(self)
        self.hide_gui = False
        self.accept("`", self.hide_editor_gui)

        self.mouse_lock = None
        self.rot_cam = None
        self.nt_printer = None
        self.nt_gui = None

        self.fov_wheel = FovScrollWheel()
        self.node_mover = NodeMover(camera)
        self.node_selector = NodeSelector(self.node_mover)

        if mouse_lock:
            self.mouse_lock = MouseWindowLock()
        if rot_cam:
            self.rot_cam = RotationalCamera()
        if nt_printer:
            self.nt_printer = NodeTransformPrinter(*get_transform_data(camera))
            self.nt_gui = NodeTransformPrinterGUI(
                self.node_mover, self.nt_printer, base.a2dLeftCenter)

        self.gui_classes = [
            self.nt_gui, self.mouse_lock
        ]

    def hide_editor_gui(self):
        self.hide_gui = not self.hide_gui

        for _class in self.gui_classes:
            for gui in _class.guis:
                if self.hide_gui:
                    gui.hide()
                else:
                    gui.show()

    def get_node_mover(self):
        return self.node_mover

    def cleanup(self):
        classes = [self.node_mover, self.node_selector, self.fov_wheel]
        if self.mouse_lock:
            classes.append(self.mouse_lock)
        if self.orb_cam:
            classes.append(self.orb_cam)
        if self.nt_printer:
            classes.append(self.nt_printer)

        for class_item in classes:
            class_item.cleanup()