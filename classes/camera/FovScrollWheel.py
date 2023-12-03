"""
Adjust the Camera Fov by scrolling the Mouse Wheel.
Limited range between 0-180.
"""
from direct.showbase.DirectObject import DirectObject

from classes.globals import Globals as G

SCROLL_AMOUNT = G.FOV_SCROLL_AMOUNT
MINIMUM_FOV = G.MINIMUM_SCROLL_FOV + G.FOV_SCROLL_AMOUNT
MAXIMUM_FOV = G.MAXIMUM_SCROLL_FOV - G.FOV_SCROLL_AMOUNT


class FovScrollWheel(DirectObject):

    def __init__(self, camera):
        DirectObject.__init__(self)

        self.accept(G.MOUSE_WHEEL_UP, self.zoom_in)
        self.accept(G.MOUSE_WHEEL_DOWN, self.zoom_out)

    def zoom_in(self):
        fov = base.camLens.getFov()[0]
        if fov >= MINIMUM_FOV:
            smaller_fov = fov - SCROLL_AMOUNT
            base.camLens.setFov(smaller_fov)

    def zoom_out(self):
        fov = base.camLens.getFov()[0]
        if fov <= MAXIMUM_FOV:
            bigger_fov = fov + SCROLL_AMOUNT
            base.camLens.setFov(bigger_fov)

    def cleanup(self):
        self.ignore_all()