"""
Modify the H and P values of the camera with mouse movement.
Enable and Disable the Mode with the RMB.
"""
from direct.showbase.DirectObject import DirectObject
from panda3d.core import WindowProperties

from classes.globals import Globals as G

MOUSE_SENSITIVITY = G.ORBITAL_CAM_MOUSE_SENSITIVITY


class OrbitalCamera(DirectObject):

    def __init__(self):
        DirectObject.__init__(self)
        self.window_properties = WindowProperties()
        self.enable = False

        base.disable_mouse()
        self.enable_orb_cam()
        base.win.requestProperties(self.window_properties)

        self.accept(G.RIGHT_MOUSE_BUTTON, self.enable_or_disable_orb_cam)

    def enable_or_disable_orb_cam(self):
        if self.enable:
            self.enable_orb_cam()
        else:
            self.disable_orb_cam()

        base.win.requestProperties(self.window_properties)
        self.enable = not self.enable

    def enable_orb_cam(self):
        self.window_properties.setCursorHidden(True)
        self.recenter_mouse_cursor()

        # doLater gives the cursor time to re-center. This prevents a sudden camera jump when re-enabling the orb cam.
        taskMgr.doMethodLater(G.TINY_DELAY, self.turn_camera_based_on_mouse_movements, G.ORB_CAM_TASK)
    
    def disable_orb_cam(self):
        self.window_properties.setCursorHidden(False)
        taskMgr.remove(G.ORB_CAM_TASK)

    def recenter_mouse_cursor(self):
        mouse_x_center, mouse_y_center = [base.win.getXSize() // 2, base.win.getYSize() // 2]
        base.win.move_pointer(0, mouse_x_center, mouse_y_center)

    def turn_camera_based_on_mouse_movements(self, task):
        self.recenter_mouse_cursor()
        self.update_cam_orientation()
        return task.cont

    def update_cam_orientation(self):
        if base.mouseWatcherNode.hasMouse():
            x_pos = base.mouseWatcherNode.get_mouse_x()
            y_pos = base.mouseWatcherNode.get_mouse_y()

            # based on where the mouse has moved from the center, modify the camera orientation
            new_cam_h_value = camera.getH() - (x_pos * MOUSE_SENSITIVITY)
            new_cam_p_value = camera.getP() + (y_pos * MOUSE_SENSITIVITY)

            camera.setH(new_cam_h_value)
            camera.setP(new_cam_p_value)

    def cleanup(self):
        if not self.mouse_visibility:
            self.change_mouse_mode()
        self.ignoreAll()