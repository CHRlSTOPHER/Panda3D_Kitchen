import tkinter as tk
from tkinter import filedialog

from direct.gui.DirectGui import DirectFrame, DirectButton

from classes.props.PlaneModel import PlaneModel

FRAME_POS = (-1.5, 0, -.5)
FRAME_SCALE = (-.295, .5, .5)

ADD_POS = (.03, 0, -.82)
ADD_SCALE = (.6, .3, .3)


class AddItemsMenu(DirectFrame):

    def __init__(self):
        frame = PlaneModel("resources/editor/maps/handle.png")
        DirectFrame.__init__(self, geom=frame,
                             pos=FRAME_POS, scale=FRAME_SCALE)
        self.initialiseoptions(AddItemsMenu)

        self.file_location = None

        self.load_buttons()

    def load_buttons(self):
        self.add_button = DirectButton(text="+", parent=self, pad=(.7, 0),
                                       pos=ADD_POS, scale=ADD_SCALE,
                                       command=self.find_file)

    def find_file(self):
        root = tk.Tk()
        root.withdraw()  # Hide the tk box that pops up.
        file_location = filedialog.askopenfilename()
        root.destroy()

        # get the proper resource path from the file location
        add_folder = False
        real_file_location = ""
        for folder in file_location.split("/"):
            if add_folder:
                real_file_location += folder + "/"
            if folder == 'resources':
                add_folder = True

        self.file_location = real_file_location[:-1]