from panda3d.core import WindowProperties

from classes.globals import GUIGlobals as GG


class DataPrinterWindow():

    def __init__(self):
        self.wp = WindowProperties()
        self.make_second_window()

    def make_second_window(self):
        self.wp.set_origin(GG.DP_WINDOW_ORIGIN)
        self.wp.set_undecorated(True)
        self.window = base.open_window(props=self.wp, size=GG.DP_WINDOW_SIZE)