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
from classes.actors.Toon import Toon
from classes.editors.MasterEditor import MasterEditor


class Thumbnail(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        base.disable_mouse()

        # self.editor = MasterEditor(rot_cam=False)

        self.load_actors()
        self.load_attributes()

    def load_actors(self):
        # c for color lol
        c = 1
        t = 8
        self.pink = Toon(render, 'm', "~self.pink", 1000,
                         'pss', 's', 'm', 'shorts',
                         t, t, 7, c, c, c, c, 41, c, c, True)
        surprise_texture = loader.load_texture(
            "phase_3/maps/eyesSurprised.jpg",
            "phase_3/maps/eyesSurprised_a.rgb",
        )
        self.pink.disable_autowalker()

        self.pink.find('**/eyes-short').set_texture(surprise_texture, 1)
        self.pink.change_muzzle('surprise')
        self.pink.pose("slip-forward", 45)

    def load_attributes(self):
        self.pink.set_pos_hpr(0.51, 1.55, 1.0, -2.25, 48.41, 0.0)
        self.pink.get_part("head").set_pos_hpr(0.0, 0.0, 0.0, 17.25, 3.75, 6.75)
        self.pink.right_eye.set_pos_hpr(0.07, 0.11, -0.19, 15.0, 21.62, 0.0)
        self.pink.left_eye.set_pos_hpr(-0.1, 0.07, -0.17, -12.75, 18.75, 0.0)
        camera.set_pos_hpr(1.21, 4.18, 2.3, -203.2, 1.81, 0.0)

Thumbnail().run()