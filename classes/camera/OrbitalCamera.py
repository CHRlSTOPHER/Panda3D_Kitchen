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
        self.toggle_value = True
        self.cam_task = True

        base.disable_mouse()
        self.toggle_orb_cam()
        self.accept(G.RIGHT_MOUSE_BUTTON, self.toggle_orb_cam)

    def toggle_orb_cam(self):
        self.window_properties.setCursorHidden(self.toggle_value)

        if self.toggle_value:
            self.recenter_mouse_cursor()
            taskMgr.doMethodLater(G.TINY_DELAY, self.orb_cam_task, G.ORB_CAM_TASK)
        else:
            taskMgr.remove(G.ORB_CAM_TASK)

        base.win.requestProperties(self.window_properties)
        self.toggle_value = not self.toggle_value

    def recenter_mouse_cursor(self):
        mouse_x_center, mouse_y_center = [base.win.getXSize() // 2, base.win.getYSize() // 2]
        base.win.move_pointer(0, mouse_x_center, mouse_y_center)

    def orb_cam_task(self, task):
        if self.cam_task:
            self.recenter_mouse_cursor()
            self.update_cam_orientation()
            return task.cont
        else:
            return task.done

    def update_cam_orientation(self):
        if base.mouseWatcherNode.hasMouse():
            x_pos = base.mouseWatcherNode.get_mouse_x()
            y_pos = base.mouseWatcherNode.get_mouse_y()

            # based on where the mouse has moved from the center, modify the camera orientation
            # also factor fov into the equation.
            # if the fov is very small, reduce the movement. Easier viewing close up.
            fov_mod = base.camLens.getFov()[0] / G.FOV_MODIFIER
            new_cam_h_value = camera.getH() - (x_pos * MOUSE_SENSITIVITY * fov_mod)
            new_cam_p_value = camera.getP() + (y_pos * MOUSE_SENSITIVITY * fov_mod)
            #print(MOUSE_SENSITIVITY)
            #print(new_cam_p_value)

            camera.setH(new_cam_h_value)
            camera.setP(new_cam_p_value)

    def cleanup(self):
        if not self.toggle_value:
            self.toggle_orb_cam()
        self.cam_task = False
        self.ignoreAll()