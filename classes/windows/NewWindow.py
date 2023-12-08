"""
Creates a new window. New camera, render, render2d, and aspect2d.
"""
from panda3d.core import (WindowProperties, MouseAndKeyboard, MouseWatcher,
                          NodePath, PGTop)


class NewWindow(WindowProperties):

    def __init__(self, origin, size, undecorated=True, name=""):
        WindowProperties.__init__(self)
        self.name = name
        self.setup_window(origin, size, undecorated)
        self.setup_render2d()
        self.setup_mouse_watcher()

    def setup_window(self, origin, size, undecorated):
        self.set_origin(origin)
        self.set_undecorated(undecorated)
        self.window = base.open_window(props=self, size=size)

    def setup_render2d(self):
        self.render = NodePath('dp_render')
        base.camList[-1].reparentTo(self.render)

        self.render2d = NodePath('dp_render2d')
        self.camera2d = base.make_camera2d(self.window)
        self.camera2d.reparent_to(self.render2d)
        self.render2d.setDepthTest(0)
        self.render2d.setDepthWrite(0)
        self.render2d.setMaterialOff(1)
        self.render2d.setTwoSided(1)

        self.aspect2d = self.render2d.attachNewNode(PGTop('myAspect2d'))
        aspectRatio = base.camList[-1].node().get_lens().getAspectRatio()

        self.aspect2d.setScale(1.0 / aspectRatio, 1.0, 1.0)

        self.a2dBackground = self.aspect2d.attachNewNode("a2dBackground")

        #: The Z position of the top border of the aspect2d screen.
        self.a2dTop = 1.0
        #: The Z position of the bottom border of the aspect2d screen.
        self.a2dBot = -1.0
        #: The X position of the left border of the aspect2d screen.
        self.a2dLeft = -aspectRatio
        #: The X position of the right border of the aspect2d screen.
        self.a2dRight = aspectRatio

        self.a2dTopCenter = self.aspect2d.attachNewNode("a2dTopCenter")
        self.a2dTopCenterNs = self.aspect2d.attachNewNode("a2dTopCenterNS")
        self.a2dBotCenter = self.aspect2d.attachNewNode("a2dBotCenter")
        self.a2dBotCenterNs = self.aspect2d.attachNewNode("a2dBotCenterNS")
        self.a2dLeftCenter = self.aspect2d.attachNewNode("a2dLeftCenter")
        self.a2dLeftCenterNs = self.aspect2d.attachNewNode("a2dLeftCenterNS")
        self.a2dRightCenter = self.aspect2d.attachNewNode("a2dRightCenter")
        self.a2dRightCenterNs = self.aspect2d.attachNewNode("a2dRightCenterNS")

        self.a2dTopLeft = self.aspect2d.attachNewNode("a2dTopLeft")
        self.a2dTopLeftNs = self.aspect2d.attachNewNode("a2dTopLeftNS")
        self.a2dTopRight = self.aspect2d.attachNewNode("a2dTopRight")
        self.a2dTopRightNs = self.aspect2d.attachNewNode("a2dTopRightNS")
        self.a2dBotLeft = self.aspect2d.attachNewNode("a2dBotLeft")
        self.a2dBotLeftNs = self.aspect2d.attachNewNode("a2dBotLeftNS")
        self.a2dBotRight = self.aspect2d.attachNewNode("a2dBotRight")
        self.a2dBotRightNs = self.aspect2d.attachNewNode("a2dBotRightNS")

        # Put the nodes in their places
        self.a2dTopCenter.setPos(0, 0, self.a2dTop)
        self.a2dTopCenterNs.setPos(0, 0, self.a2dTop)
        self.a2dBotCenter.setPos(0, 0, self.a2dBot)
        self.a2dBotCenterNs.setPos(0, 0, self.a2dBot)
        self.a2dLeftCenter.setPos(self.a2dLeft, 0, 0)
        self.a2dLeftCenterNs.setPos(self.a2dLeft, 0, 0)
        self.a2dRightCenter.setPos(self.a2dRight, 0, 0)
        self.a2dRightCenterNs.setPos(self.a2dRight, 0, 0)

        self.a2dTopLeft.setPos(self.a2dLeft, 0, self.a2dTop)
        self.a2dTopLeftNs.setPos(self.a2dLeft, 0, self.a2dTop)
        self.a2dTopRight.setPos(self.a2dRight, 0, self.a2dTop)
        self.a2dTopRightNs.setPos(self.a2dRight, 0, self.a2dTop)
        self.a2dBotLeft.setPos(self.a2dLeft, 0, self.a2dBot)
        self.a2dBotLeftNs.setPos(self.a2dLeft, 0, self.a2dBot)
        self.a2dBotRight.setPos(self.a2dRight, 0, self.a2dBot)
        self.a2dBotRightNs.setPos(self.a2dRight, 0, self.a2dBot)

    def setup_mouse_watcher(self):
        self.keyboard = base.dataRoot.attachNewNode(
            MouseAndKeyboard(self.window, 0, 'NW_mk_' + self.name))
        self.mouse_watcher = self.keyboard.attachNewNode(
            MouseWatcher('NW_mw_' + self.name))
        self.aspect2d.node().setMouseWatcher(self.mouse_watcher.node())

    def cleanup(self):
        pass