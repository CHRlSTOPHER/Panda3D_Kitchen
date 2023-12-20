import os, sys
# The code below lets you load the py file directly in cmd/IDE.
# (You will still need to use a version of python that comes with Panda3D)
current_path = os.getcwd()
project_path = ""
for folder in current_path.split("\\"):
    project_path += folder + "/"
    if folder == "Panda3D_Kitchen":
        break

sys.path.append(project_path)
os.chdir(project_path)

"""
Tests functionality of actors.
"""
from classes.settings import Settings

from direct.showbase.ShowBase import ShowBase

from classes.actors.Suit import Suit
from classes.actors.Toon import Toon
from classes.editors.MasterEditor import MasterEditor
from classes.globals import Globals as G
from classes.globals.ToonColors import ToonColors


class ActorTest(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.accept(G.ESCAPE, exit)
        self.master_editor = MasterEditor()

        # self.setup_cogs()
        self.setup_toons()

    def setup_cogs(self):
        self.flunky = Suit("f", render, suit_name="~self.flunky")
        self.penny = Suit("pp", render, suit_name="~self.penny")
        self.cheese = Suit("tbc", render, suit_name="~self.cheese")

        camera.set_pos_hpr(30.71, 3.51, 4.33, 76.28, -0.54, 0.0)

    def setup_toons(self):
        TC = ToonColors
        self.pink = Toon(parent=render, gender='m',
                           toon_name="~self.pink",
                           head='pss', torso='s', legs='m', bottom='shorts',
                           shirt_t=8, sleeve_t=8, bottom_t=7,
                           head_color=TC.BRIGHT_RED,
                           shirt_color=TC.BRIGHT_RED, #
                           sleeve_color=TC.BRIGHT_RED, #
                           arm_color=TC.BRIGHT_RED,
                           glove_color=TC.WHITE,
                           leg_color=TC.BRIGHT_RED,
                           bottom_color=TC.BRIGHT_RED) #

        camera.set_pos_hpr(-4.56, 4.14, 4.65, 227.25, -16.24, 0.0)


app = ActorTest()
app.run()