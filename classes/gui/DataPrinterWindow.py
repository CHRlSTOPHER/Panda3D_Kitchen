from panda3d.core import WindowProperties

from classes.globals import GUIGlobals as GG


class DataPrinterWindow():

    def __init__(self):
        self.wp = WindowProperties()
        self.wp.set_undecorated(True)
        self.make_extra_window()

    def make_extra_window(self):
        properties = base.win.getProperties()
        decorated = str(properties).split()[6]

        if decorated == "undecorated":
            self.wp.set_origin(GG.DP_WINDOW_ORIGIN_B_LESS)
            self.window = base.open_window(props=self.wp, size=GG.DP_WINDOW_SIZE_B_LESS)
        else:
            self.wp.set_origin(GG.DP_WINDOW_ORIGIN)
            self.window = base.open_window(props=self.wp, size=GG.DP_WINDOW_SIZE)