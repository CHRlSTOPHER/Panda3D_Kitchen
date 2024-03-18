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

import tkinter as tk
from tkinter import filedialog

from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton, DirectFrame

from classes.globals.AppGlobals import FILE_DATA

BUTTONS = [
    ("CREATE", (-.19, 0, -.67), [.115, .115, .115]),
    ("LOAD", (.19, 0, -.67), (.123, .12, .116)),
    ("DELETE", (-.19, 0, -.802), (.121, .121, .121)),
    ("MOVE", (.193, 0, -.802), (.115, .115, .12)),
    ("APPLICATIONS", (-.018, 0, -.925), (.116, .116, .116)),
]
FILENAMES = ["Actors", "Dialogue", "Main", "Music", "ParticleEffects",
             "Props", "Scenes", "Sounds", "TextBoxes", "Textures"]


class Startup(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.project_frame = None
        self.folder_location = None
        self.main = None
        self.commands = [
            self.create_project,
            self.load_project,
            self.delete_project,
            self.move_project,
            self.load_apps
        ]

        self.load_gui()

    def load_gui(self):
        self.project_frame = DirectFrame(pos=(0, 0, .1), scale=1.1)
        i = 0
        for name, pos, scale in BUTTONS:
            m = .9
            new_scale = (scale[0] * m, scale[1] * m, scale[2] * m)
            DirectButton(parent=self.project_frame, text=name,
                         pos=pos, scale=new_scale, command=self.commands[i])
            i += 1

    def create_project(self):
        self.define_folder_location()
        for filename in FILENAMES:
            file = f"{self.folder_location}/{filename}.py"
            if os.path.exists(file):
                print("A project already exists there!")
                return

            file = open(file, "x")
            file.write(FILE_DATA[filename])
            file.close()

    def load_project(self):
        self.define_folder_location()
        # Add directory to path in case directory is in a different location.
        sys.path.append(self.folder_location)
        from Main import Main
        self.main = Main()

    def delete_project(self):
        self.define_folder_location()
        for filename in FILENAMES:
            file = f"{self.folder_location}/{filename}.py"
            if os.path.exists(file):
                os.remove(file)

    def move_project(self):
        pass

    def load_apps(self):
        pass

    def define_folder_location(self):
        root = tk.Tk()
        root.withdraw()
        self.folder_location = filedialog.askdirectory()
        root.destroy()


project = Startup()
project.run()