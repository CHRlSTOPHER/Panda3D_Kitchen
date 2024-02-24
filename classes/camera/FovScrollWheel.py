"""
Adjust the Camera Fov by scrolling the Mouse Wheel.
Limited range between 0-180.
"""
from direct.showbase.DirectObject import DirectObject

from classes.globals import Globals as G

SCROLL_AMOUNT = int(G.FOV_SCROLL_AMOUNT)
MINIMUM_FOV = G.MINIMUM_SCROLL_FOV + G.FOV_SCROLL_AMOUNT
MAXIMUM_FOV = G.MAXIMUM_SCROLL_FOV - G.FOV_SCROLL_AMOUNT\

class FovScrollWheel(DirectObject):

    def __init__(self, fov):
        DirectObject.__init__(self)
        self.current_fov = fov
        self.new_fov = fov
        self.fov_increment = 1

        self.accept(G.MOUSE_WHEEL_UP, self.zoom_in)
        self.accept(G.MOUSE_WHEEL_DOWN, self.zoom_out)

    def zoom_in(self):
        if self.new_fov - SCROLL_AMOUNT >= MINIMUM_FOV:
            self.new_fov = self.new_fov - SCROLL_AMOUNT
            base.camLens.set_fov(self.new_fov)

    def zoom_out(self):
        if self.new_fov + SCROLL_AMOUNT <= MAXIMUM_FOV:
            self.new_fov = self.new_fov + SCROLL_AMOUNT
            base.camLens.set_fov(self.new_fov)

    def cleanup(self):
        self.ignore_all()