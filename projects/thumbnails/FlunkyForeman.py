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
Loads the OG 151 Pokémon as sprites.
Organizes them in a vertically rectangular shape.
"""
from classes.settings import Settings

from direct.showbase.ShowBase import ShowBase

from classes.editors.MasterEditor import MasterEditor
from classes.globals import Globals as G
from classes.actors.Suit import Suit
from classes.editors.MasterEditor import MasterEditor

SCENE = 1


class Thumbnail(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        base.disable_mouse()

        self.editor = MasterEditor(rot_cam=True, mouse_lock=False)

        camera.set_pos_hpr(11.09, 3.66, 4.51, -245.42, 3.84, -4.0)
        base.camLens.set_fov(52.0)

        self.load_actors()
        self.load_scene()
        # self.load_attributes()

    def load_actors(self):
        self.ff = Suit('ff', render, suit_name='~foreman')
        self.f = Suit('f', render, suit_name='~flunky')

        foreman_glasses = self.ff.find('**/sellbotForemanGlasses')
        flunky_glasses = self.f.glasses

        foreman_glasses.set_scale(1.3)
        flunky_glasses.set_scale(.75)

        foreman_glasses.set_name("~sellbotForemanGlasses")
        flunky_glasses.set_name("~glasses")

        foreman_glasses.reparent_to(self.f.find('**/joint_head'))
        flunky_glasses.reparent_to(self.ff.find('**/joint_head'))

        if SCENE == 1:
            self.f.set_pos_hpr(4.41, 5.65, 0.38, -13.5, 2.25, 3.75)
            self.f.head.set_pos_hpr(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
            foreman_glasses.set_pos_hpr(0.0, 0.4, -0.93, 0.0, 10.5, 0.0)
            self.ff.set_pos_hpr(-1.92, -0.69, 0.09, -31.5, 0.0, 3.75)
            self.ff.find('**/ttr_m_ene_sellbotForeman').set_pos_hpr(0.0, 0.0, 0.0,
                                                                    0.0, 0.0, 0.0)
            flunky_glasses.set_pos_hpr(0.0, -0.13, 0.6, 0.0, 0.0, 0.0)
            self.f.left_eye.set_pos_hpr(0.37, 0.56, 0.5, -0.0, 0.0, -0.0)
            self.f.right_eye.set_pos_hpr(-0.14, 0.56, 0.5, -0.0, 0.0, -0.0)
            camera.set_pos_hpr(5.72, 10.32, 5.08, -200.68, -0.43, -4.0)
        else:
            pass

    def load_scene(self):
        factory = loader.load_model('SelbotLegFactory.bam')
        factory.reparent_to(render)
        factory.set_pos_hpr(243.26, 691.06, -208.72, -200.57, 0.0, -3.75)


Thumbnail().run()