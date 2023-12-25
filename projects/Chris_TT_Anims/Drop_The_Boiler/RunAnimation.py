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
Using the Drop gag on the Boiler Boss. (Meme Video)
'''
from direct.showbase.ShowBase import ShowBase

from classes.editors.MasterEditor import MasterEditor
# from .UnpaidProps import

class RunAnimation(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)
        self.master_editor = MasterEditor(mouse_lock=False)
        self.test_scene()

    def test_scene(self):
        # If we import earlier, we cannot load Toons and Suits with Showbase.
        from Paid_Actors import Actors
        Actors.pink.set_pos_hpr(0.0, 18.77, 0.0, 178.68, 0.0, 0.0)
        # Actors.boiler.set_pos_hpr(0.0, -11.15, 0.0, -180, 0.0, 0.0)
        camera.set_pos_hpr(-20.4, 53.63, 6.21, -162.36, 2.81, 0.0)


RunAnimation().run()