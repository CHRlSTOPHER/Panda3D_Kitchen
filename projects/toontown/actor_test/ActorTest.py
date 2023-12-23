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
        self.node_mover = self.master_editor.get_node_mover()

        camera.set_pos_hpr(-6.95, 6.25, 3.81, 227.61, -13.86, 0.0)

        self.pink = Toon(parent=render, gender='m',
                           toon_name="~self.pink",
                           head='pss', torso='s', legs='m', bottom='shorts',
                           shirt_t=8, sleeve_t=8, bottom_t=7,
                           head_color=TC.BRIGHT_RED,
                           shirt_color=TC.BRIGHT_RED,
                           sleeve_color=TC.BRIGHT_RED,
                           arm_color=TC.BRIGHT_RED,
                           glove_color=TC.WHITE,
                           leg_color=TC.BRIGHT_RED,
                           bottom_color=TC.BRIGHT_RED)
        # self.pink.get_part('torso').hide()
        self.pink.set_pos_hpr(-0.33, 1.45, 3.08, 17.98, -35.52, -4.5)
        camera.set_pos_hpr(-7.4, 5.65, 7.26, 236.97, -25.74, 0.0)

        self.pink.load_ragdoll()

app = ActorTest()
app.run()