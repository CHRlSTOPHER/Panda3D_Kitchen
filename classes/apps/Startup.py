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
Make a new project. Load an existing project.
Move a project. Delete a project.
Start a side application like Make-a-Toon
"""
from classes.settings import Settings

from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton, DirectFrame

BUTTONS = [
    ("CREATE", (-.19, 0, -.67), [.115, .115, .115]),
    ("LOAD", (.19, 0, -.67), (.123, .12, .116)),
    ("DELETE", (-.19, 0, -.802), (.121, .121, .121)),
    ("MOVE", (.193, 0, -.802), (.115, .115, .12)),
    ("APPLICATIONS", (-.018, 0, -.925), (.116, .116, .116)),
]


class Startup(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.project_frame = None

        self.load_gui()

    def load_gui(self):
        self.project_frame = DirectFrame(pos=(0, 0, .1), scale=1.1)
        for name, pos, scale in BUTTONS:
            m = .9
            new_scale = (scale[0] * m, scale[1] * m, scale[2] * m)
            DirectButton(parent=self.project_frame, text=name,
                         pos=pos, scale=new_scale)


project = Startup()
project.run()