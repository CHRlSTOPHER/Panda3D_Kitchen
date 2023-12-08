"""
Adjust the Camera Fov by scrolling the Mouse Wheel.
Limited range between 0-180.
"""
from direct.showbase.DirectObject import DirectObject

from classes.globals import Globals as G

SCROLL_AMOUNT = int(G.FOV_SCROLL_AMOUNT)
MINIMUM_FOV = G.MINIMUM_SCROLL_FOV + G.FOV_SCROLL_AMOUNT
MAXIMUM_FOV = G.MAXIMUM_SCROLL_FOV - G.FOV_SCROLL_AMOUNT
SMOOTH_FOV_TASK = "smooth_fov_task"

class FovScrollWheel(DirectObject):

    def __init__(self):
        DirectObject.__init__(self)
        self.current_fov = G.BASE_FOV
        self.new_fov = G.BASE_FOV
        self.fov_increment = 1

        self.accept(G.MOUSE_WHEEL_UP, self.zoom_in)
        self.accept(G.MOUSE_WHEEL_DOWN, self.zoom_out)
        taskMgr.add(self.smooth_fov_transitions, SMOOTH_FOV_TASK)

    def zoom_in(self):
        if self.new_fov - SCROLL_AMOUNT >= MINIMUM_FOV:
            self.new_fov = self.new_fov - SCROLL_AMOUNT

    def zoom_out(self):
        if self.new_fov + SCROLL_AMOUNT <= MAXIMUM_FOV:
            self.new_fov = self.new_fov + SCROLL_AMOUNT

    def smooth_fov_transitions(self, task):
        if base.camLens.get_fov()[0] == self.new_fov:
            return task.again

        increment = self.fov_increment
        if self.current_fov > self.new_fov:
            increment = -self.fov_increment

        self.current_fov += increment
        base.camLens.set_fov(self.current_fov)

        return task.again

    def cleanup(self):
        taskMgr.remove(SMOOTH_FOV_TASK)
        self.ignore_all()