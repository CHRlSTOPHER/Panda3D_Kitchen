import os, sys

from panda3d.core import Fog

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
Loads the OG 151 Pokémon as sprites.
Organizes them in a vertically rectangular shape.
"""
from classes.settings import Settings

from direct.showbase.ShowBase import ShowBase

from classes.editors.MasterEditor import MasterEditor
from classes.globals import Globals as G
from classes.actors.Suit import Suit
from classes.editors.MasterEditor import MasterEditor


class Thumbnail(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        base.disable_mouse()

        self.editor = MasterEditor(rot_cam=False, )

        camera.set_pos_hpr(11.09, 3.66, 4.51, -245.42, 3.84, -4.0)
        base.camLens.set_fov(52.0)

        self.load_actors()
        # self.load_scene()
        # self.load_attributes()

    def load_actors(self):
        self.bp = Suit('cp', render)
        self.lc = Suit('lc', render)
        self.ma = Suit('ma', render)
        self.ff = Suit('ff', render)

        self.bp.set_pos_hpr(5.88, -0.33, 0.0, 0.0, 0.0, 0.0)
        self.bp.head.find('**/ttr_m_ene_bossbotClubPresident').set_pos_hpr(
            0.0, 0.0, 0.0, -49.23, -9.0, -6.0)
        self.ma.set_pos_hpr(0.71, -0.96, 0.0, -23.25, 0.0, 0.0)
        self.ma.head.find('**/ttr_m_ene_cashbotAuditor').set_pos_hpr(
            0.0, 0.0, 0.0, -44.25, -12.75, -12.0)
        self.ff.set_pos_hpr(-1.78, 0.53, 0.0, -27.75, 0.0, 0.0)
        self.ff.head.find('**/ttr_m_ene_sellbotForeman').set_pos_hpr(
            0.0, 0.0, 0.0, -49.5, -16.5, -1.5)
        self.lc.set_pos_hpr(-4.89, 1.69, 0.0, -43.5, 0.0, 0.0)
        self.lc.head.find('**/ttr_m_ene_lawbotClerk').set_pos_hpr(
            0.0, 0.0, 0.0, -51.5, -21.32, 0.0)

    def load_scene(self):
        room = loader.load_model("phase_5/models/cogdominium/ttr_m_ara_cbr_barrelRoom.bam")
        room.reparent_to(render)

        myFog = Fog("Barrel Room Fog")
        myFog.setColor(.05, .025, .025)
        myFog.setExpDensity(.01)
        render.setFog(myFog)

        room.set_pos_hpr(-4.21, -2.42, -5.63, -95.27, -4.33, 2.25)


Thumbnail().run()