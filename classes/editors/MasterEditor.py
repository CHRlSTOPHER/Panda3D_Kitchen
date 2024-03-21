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

    def __init__(self, cameras=[], mouse_watcher=None,
                 display_region=None, _render=False,
                 rot_cam=True, nt_printer=True, fov=None, sequence=None):
        DirectObject.__init__(self)

        self.cameras = []
        self.mouse_watcher = mouse_watcher
        self.display_region = display_region
        self.fov = None

        self.hide_gui = False

        if _render:
            self.render = _render
        else:
            self.render = render

        self.rot_cam = rot_cam
        self.nt_printer = None
        self.nt_gui = None

        if cameras:
            self.set_camera(cameras[-1])
        else:
            self.set_camera(camera)

        if nt_printer:
            self.nt_printer = NodeTransformPrinter(*get_transform_data(camera))
            self.nt_gui = NodeTransformPrinterGUI(
                self.node_mover, self.nt_printer, base.a2dLeftCenter)

        if sequence:
           self.sequence_manager = SequenceManager(sequence)

        self.accept("`", self.hide_editor_gui)

    def set_camera(self, camera):
        self.rot_cam = RotationalCamera(camera, self.rot_cam)
        self.fov_wheel = FovScrollWheel(camera, self.fov)
        self.node_mover = NodeMover(camera, camera)
        self.node_selector = NodeSelector(camera, self.render,
                                          self.mouse_watcher, self.node_mover)

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

        for selector in self.node_selectors:
            selector.cleanup()

        for class_item in classes:
            class_item.cleanup()