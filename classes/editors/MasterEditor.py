"""
A collection of different classes. Mashes them together into an editor.
"""
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectFrame

from classes.camera.RotationalCamera import RotationalCamera
from classes.camera.FovScrollWheel import FovScrollWheel
from .NodeMover import NodeMover
from .NodeSelector import NodeSelector
from .SequenceManager import SequenceManager


class MasterEditor(DirectObject):

    def __init__(self, cameras=[], mouse_watcher=None,
                 display_region=None, _render=False,
                 rot_cam=True, fov=None, sequence=None):
        DirectObject.__init__(self)

        self.cameras = []
        self.mouse_watcher = mouse_watcher
        self.display_region = display_region

        self.render = render
        if _render: # Add the new render made for a new display region.
            self.render = _render

        self.rot_cam = rot_cam
        self.fov = fov

        if sequence:
           self.sequence_manager = SequenceManager(sequence)

        self.hide_gui = False

        if cameras: # Get the last camera from the list
            self.set_camera(cameras[-1])
        else: # Default to og camera.
            self.set_camera(camera)

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

        for selector in self.node_selectors:
            selector.cleanup()

        for class_item in classes:
            class_item.cleanup()