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
from direct.interval.IntervalGlobal import Sequence, Wait, Func

from classes.actors.Suit import Suit
from classes.actors.Toon import Toon
from classes.editors.MasterEditor import MasterEditor
from classes.globals import Globals as G
from classes.globals.ToonColors import ToonColors

TC = ToonColors


class ActorTest(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.accept(G.ESCAPE, exit)
        base.set_background_color(.1, .1, .1, 1)
        base.disable_mouse()

        self.master_editor = MasterEditor(rot_cam=True, mouse_lock=False)

        self.pink = Toon(parent=render, gender='m',
                           toon_name="~self.pink",
                           head='pss', torso='s', legs='m', bottom='shorts',
                           shirt_t=8, sleeve_t=8, bottom_t=7,
                           head_color=1,
                           shirt_color=1,
                           sleeve_color=1,
                           arm_color=1,
                           glove_color=41,
                           leg_color=1,
                           bottom_color=1)

        self.suit = Suit('pp', render, suit_name="!self.suit")

        self.pink.set_pos_hpr(-0.52, 2.43, 0.0, 77.91, 0.0, 0.0)
        self.suit.set_pos_hpr(-2.54, -0.27, 0.0, 31.5, 0.0, 0.0)
        camera.set_pos_hpr(-12.7, 8.12, 4.45, 238.19, -9.29, 0.0)


app = ActorTest()
app.run()