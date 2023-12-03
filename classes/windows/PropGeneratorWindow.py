from classes.windows.NewWindow import NewWindow
from classes.globals import GUIGlobals as GG


class PropGeneratorWindow(NewWindow):

    def __init__(self, node_mover):
        self.node_mover = node_mover

        self.generate_window()


    def generate_window(self):
        properties = base.win.getProperties()
        decorated = str(properties).split()[6]
        if decorated == "undecorated":
            NewWindow.__init__(self, GG.PG_WINDOW_ORIGIN_B_LESS, GG.PG_WINDOW_SIZE_B_LESS)
        else:
            NewWindow.__init__(self, GG.PG_WINDOW_ORIGIN, GG.PG_WINDOW_SIZE)