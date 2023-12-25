# The code below lets you load the py file directly in cmd/IDE.
# (You will still need to use a version of python that comes with Panda3D)
import os, sys

current_path = os.getcwd()
project_path = ""
for folder in current_path.split("\\"):
    project_path += folder + "/"
    if folder == "Panda3D_Kitchen":
        break

sys.path.append(project_path)
os.chdir(project_path)
from classes.settings import Settings

'''
An application that lets you create new Toons and save them to a json file.
Or you can load an existing Toon from the json file and edit it!
'''
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import TransparencyAttrib

from classes.actors.Toon import Toon
from classes.globals import Globals as G
from classes.globals import ToonGlobals as TG
from classes.globals.ToonColors import ToonColors as TC
from classes.props.PlaneModel import PlaneModel
from classes.editors.MasterEditor import MasterEditor

FRAME_TEXTURE = G.MAPS_3 + "tt_t_gui_ups_panelBg"


class Make_A_Toon_GUI(DirectFrame):

    def __init__(self):
        DirectFrame.__init__(self)
        self.initialiseoptions(Make_A_Toon_GUI)

        self.edit_toon = False
        self.create_toon = False
        self.toon = None

        self.gender = 'm'
        self.limbs = ['dss', 'm', 'm', 'shorts']
        self.colors = [41, 41, 41, 41, 41, 41, 41] # White = 41
        self.clothes = [0, 0, 0]
        self.name = ""

        self.load_main_frame()

        # each function returns a list of gui.
        self.pages = [
            self.options_page(),
            self.gender_page(),
            self.species_page(),
            self.limbs_page(),
            self.colors_page(),
            self.clothes_page(),
            self.name_page()
        ]
        self.load_toon()
        self.show_page(0)

    def load_main_frame(self):
        textures = [FRAME_TEXTURE + ".jpg", FRAME_TEXTURE + "_a.rgb"]
        self.frame = DirectFrame(parent=base.a2dLeftCenter,
                                 geom=PlaneModel(textures),
                                 frameVisibleScale=(0, 0), pos=(1.0, 0, 0))

    def options_page(self):
        return []

    def gender_page(self):
        return []

    def species_page(self):
        return []

    def limbs_page(self):
        return []

    def colors_page(self):
        return []

    def clothes_page(self):
        return []

    def name_page(self):
        return []

    def load_toon(self):
        if self.toon:
            self.toon.delete()
        L, CO, CL = [self.limbs, self.colors, self.clothes]
        self.toon = Toon(render, self.gender, toon_name=self.name, lod=1000,
                         head=L[0], torso=L[1], legs=L[2], bottom=L[3],
                         shirt_t=CL[0], sleeve_t=CL[1], bottom_t=CL[2],
                         head_color=CO[0], shirt_color=CO[1],
                         sleeve_color=CO[2], glove_color=CO[3],
                         leg_color=CO[4], bottom_color=CO[5])

    def show_page(self, index):
        for page in self.pages:
            for gui_node in page:
                gui_node.hide() # hide all gui

        for gui_node in self.pages[index]:
            gui_node.show() # show desired page gui

class Make_A_Toon(ShowBase, Make_A_Toon_GUI):

    def __init__(self):
        ShowBase.__init__(self)
        Make_A_Toon_GUI.__init__(self)
        base.disable_mouse()
        camera.set_pos_hpr(-3.5, 12.0, 3.0, -150.0, -4.0, 0.0)
        # self.master_editor = MasterEditor()


Make_A_Toon().run()